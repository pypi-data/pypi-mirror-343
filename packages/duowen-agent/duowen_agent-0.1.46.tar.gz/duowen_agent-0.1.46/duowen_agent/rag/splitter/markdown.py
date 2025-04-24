import re
from typing import TypedDict, List, Dict

from duowen_agent.llm import tokenizer
from duowen_agent.rag.models import Document
from .base import BaseChunk


class MarkdownProcessor:
    def __init__(self, markdown_text):
        self.markdown_text = markdown_text
        self.code_block_pattern = re.compile(r"```.*?```", re.DOTALL)  # 匹配代码块
        self.atx_heading_pattern = re.compile(
            r"^(#{1,6})\s+(.+)$", re.MULTILINE
        )  # # 格式标题
        self.setext_heading_pattern = re.compile(
            r"^(.+)\n=+$|^(.+)\n-+$", re.MULTILINE
        )  # = 和 - 格式标题

    def _is_in_code_block(self, position):
        """检查某个位置是否在代码块中"""
        for match in self.code_block_pattern.finditer(self.markdown_text):
            if match.start() <= position < match.end():
                return True
        return False

    def _is_valid_setext_heading(self, match):
        """检查 = 和 - 格式的标题是否合法"""
        heading_text = match.group(1) or match.group(2)  # 获取标题文本
        underline_line = match.group(0).split("\n")[1]  # 获取 = 或 - 行
        # 检查 = 或 - 的长度是否至少与标题文本长度相同
        return len(underline_line) >= len(heading_text.strip())

    def convert_underline_headings(self):
        """
        将 Markdown 中的 `=` 和 `-` 格式的标题转换为 `#` 格式的标题。
        - `=` 替换为 `#`
        - `-` 替换为 `##`
        - 排除代码块中的内容。
        """

        def replace_heading(match):
            if self._is_in_code_block(match.start()):
                return match.group(0)  # 如果在代码块中，直接返回原内容
            if not self._is_valid_setext_heading(match):
                return match.group(0)  # 如果标题不合法，直接返回原内容
            heading_text = match.group(1) or match.group(2)
            if match.group(0).endswith("="):
                return f"# {heading_text.strip()}"  # 一级标题
            else:
                return f"## {heading_text.strip()}"  # 二级标题

        self.markdown_text = self.setext_heading_pattern.sub(
            replace_heading, self.markdown_text
        )
        return self.markdown_text

    def count_headings(self):
        """统计 Markdown 文档中的标题数量"""
        # 移除代码块
        text_without_code_blocks = self.code_block_pattern.sub("", self.markdown_text)

        # 查找所有匹配的标题（# 格式）
        atx_headings = [
            match.group(0)
            for match in self.atx_heading_pattern.finditer(text_without_code_blocks)
            if not self._is_in_code_block(match.start())
        ]

        # 查找所有匹配的标题（= 和 - 格式），并排除代码块中的内容
        setext_headings = [
            match.group(0)
            for match in self.setext_heading_pattern.finditer(text_without_code_blocks)
            if not self._is_in_code_block(match.start())
            and self._is_valid_setext_heading(match)
        ]

        return len(atx_headings) + len(setext_headings)

    def get_top_level_heading(self):
        """
        获取 Markdown 文档中最顶级的目录是几级标签。
        - 返回最顶级标题的级别（1 表示一级标题，2 表示二级标题，依此类推）。
        - 如果没有标题，返回 None。
        """
        # 移除代码块
        text_without_code_blocks = self.code_block_pattern.sub("", self.markdown_text)

        # 存储所有标题的级别
        heading_levels = []

        # 查找所有匹配的标题（# 格式）
        for match in self.atx_heading_pattern.finditer(text_without_code_blocks):
            if not self._is_in_code_block(match.start()):
                level = len(match.group(1))  # # 的数量
                heading_levels.append(level)

        # 查找所有匹配的标题（= 和 - 格式），并排除代码块中的内容
        for match in self.setext_heading_pattern.finditer(text_without_code_blocks):
            if not self._is_in_code_block(
                match.start()
            ) and self._is_valid_setext_heading(match):
                level = 1 if match.group(0).endswith("=") else 2  # = 为一级，- 为二级
                heading_levels.append(level)

        return min(heading_levels) if heading_levels else None


class LineType(TypedDict):
    """Line type as typed dict."""

    metadata: Dict[str, str]
    content: str


class HeaderType(TypedDict):
    """Header type as typed dict."""

    level: int
    name: str
    data: str


class MarkdownHeaderTextSplitter:
    """Splitting markdown files based on specified headers."""

    def __init__(
        self, return_each_line: bool = False, strip_headers: bool = True, level: int = 7
    ):
        """Create a new MarkdownHeaderTextSplitter.

        Args:
            headers_to_split_on: Headers we want to track
            return_each_line: Return each line w/ associated headers
            strip_headers: Strip split headers from the content of the chunk
        """
        # Output line-by-line or aggregated into chunks w/ common headers
        self.return_each_line = return_each_line
        # Given the headers we want to split on,
        # (e.g., "#, ##, etc") order by length
        self.headers_to_split_on = [("#" * i, "#" * i) for i in range(1, level)]
        # Strip headers split headers from the content of the chunk
        self.strip_headers = strip_headers

    def aggregate_lines_to_chunks(self, lines: List[LineType]) -> List[Document]:
        """Combine lines with common metadata into chunks.

        Args:
            lines: Line of text / associated header metadata
        """
        aggregated_chunks: List[LineType] = []

        for line in lines:
            if (
                aggregated_chunks
                and aggregated_chunks[-1]["metadata"] == line["metadata"]
            ):
                # If the last line in the aggregated list
                # has the same metadata as the current line,
                # append the current content to the last lines's content
                aggregated_chunks[-1]["content"] += "  \n" + line["content"]
            elif (
                aggregated_chunks
                and aggregated_chunks[-1]["metadata"] != line["metadata"]
                # may be issues if other metadata is present
                and len(aggregated_chunks[-1]["metadata"]) < len(line["metadata"])
                and aggregated_chunks[-1]["content"].split("\n")[-1][0] == "#"
                and not self.strip_headers
            ):
                # If the last line in the aggregated list
                # has different metadata as the current line,
                # and has shallower header level than the current line,
                # and the last line is a header,
                # and we are not stripping headers,
                # append the current content to the last line's content
                aggregated_chunks[-1]["content"] += "  \n" + line["content"]
                # and update the last line's metadata
                aggregated_chunks[-1]["metadata"] = line["metadata"]
            else:
                # Otherwise, append the current line to the aggregated list
                aggregated_chunks.append(line)

        return [
            Document(page_content=chunk["content"], metadata=chunk["metadata"])
            for chunk in aggregated_chunks
        ]

    def split_text(self, text: str) -> List[Document]:
        """Split markdown file.

        Args:
            text: Markdown file
        """
        # Split the input text by newline character ("\n").
        lines = text.split("\n")
        # Final output
        lines_with_metadata: List[LineType] = []
        # Content and metadata of the chunk currently being processed
        current_content: List[str] = []
        current_metadata: Dict[str, str] = {}
        # Keep track of the nested header structure
        # header_stack: List[Dict[str, Union[int, str]]] = []
        header_stack: List[HeaderType] = []
        initial_metadata: Dict[str, str] = {}

        in_code_block = False
        opening_fence = ""

        for line in lines:
            stripped_line = line.strip()
            # Remove all non-printable characters from the string, keeping only visible
            # text.
            stripped_line = "".join(filter(str.isprintable, stripped_line))
            if not in_code_block:
                # Exclude inline code spans
                if stripped_line.startswith("```") and stripped_line.count("```") == 1:
                    in_code_block = True
                    opening_fence = "```"
                elif stripped_line.startswith("~~~"):
                    in_code_block = True
                    opening_fence = "~~~"
            else:
                if stripped_line.startswith(opening_fence):
                    in_code_block = False
                    opening_fence = ""

            if in_code_block:
                current_content.append(stripped_line)
                continue

            # Check each line against each of the header types (e.g., #, ##)
            for sep, name in self.headers_to_split_on:
                # Check if line starts with a header that we intend to split on
                if stripped_line.startswith(sep) and (
                    # Header with no text OR header is followed by space
                    # Both are valid conditions that sep is being used a header
                    len(stripped_line) == len(sep)
                    or stripped_line[len(sep)] == " "
                ):
                    # Ensure we are tracking the header as metadata
                    if name is not None:
                        # Get the current header level
                        current_header_level = sep.count("#")

                        # Pop out headers of lower or same level from the stack
                        while (
                            header_stack
                            and header_stack[-1]["level"] >= current_header_level
                        ):
                            # We have encountered a new header
                            # at the same or higher level
                            popped_header = header_stack.pop()
                            # Clear the metadata for the
                            # popped header in initial_metadata
                            if popped_header["name"] in initial_metadata:
                                initial_metadata.pop(popped_header["name"])

                        # Push the current header to the stack
                        header: HeaderType = {
                            "level": current_header_level,
                            "name": name,
                            "data": stripped_line[len(sep) :].strip(),
                        }
                        header_stack.append(header)
                        # Update initial_metadata with the current header
                        initial_metadata[name] = header["data"]

                    # Add the previous line to the lines_with_metadata
                    # only if current_content is not empty
                    if current_content:
                        lines_with_metadata.append(
                            {
                                "content": "\n".join(current_content),
                                "metadata": current_metadata.copy(),
                            }
                        )
                        current_content.clear()

                    if not self.strip_headers:
                        current_content.append(stripped_line)

                    break
            else:
                if stripped_line:
                    current_content.append(stripped_line)
                elif current_content:
                    lines_with_metadata.append(
                        {
                            "content": "\n".join(current_content),
                            "metadata": current_metadata.copy(),
                        }
                    )
                    current_content.clear()

            current_metadata = initial_metadata.copy()

        if current_content:
            lines_with_metadata.append(
                {
                    "content": "\n".join(current_content),
                    "metadata": current_metadata,
                }
            )

        # lines_with_metadata has each line with associated header metadata
        # aggregate these into chunks based on common metadata
        if not self.return_each_line:
            return self.aggregate_lines_to_chunks(lines_with_metadata)
        else:
            return [
                Document(page_content=chunk["content"], metadata=chunk["metadata"])
                for chunk in lines_with_metadata
            ]


class MarkdownHeaderChunker(BaseChunk):
    def __init__(self, chunk_size: int = 512):
        self.chunk_size = chunk_size

    @staticmethod
    def get_comp_doc(document: Document):

        _header = [f"{k} {v}" for k, v in document.metadata.items()]

        if len(_header) >= 2:
            _header = _header[:-1]

        return (
            "\n\n".join(_header)
            + "\n\n---------------------------\n\n"
            + document.page_content
        )

    def chunk(self, text: str) -> List[Document]:

        if MarkdownProcessor(text).count_headings() > 1:
            text = MarkdownProcessor(text).convert_underline_headings()

        else:
            return [
                Document(
                    page_content=text,
                    metadata=dict(token_count=tokenizer.emb_len(text), chunk_index=0),
                )
            ]

        _doc = []

        def _chunk(text, level):

            _data = MarkdownHeaderTextSplitter(
                strip_headers=False, level=level
            ).split_text(text)

            _current_doc = []

            for i in _data:

                if tokenizer.emb_len(self.get_comp_doc(i)) > self.chunk_size:

                    if _current_doc:
                        _doc.append("\n\n".join(_current_doc))
                        _current_doc = []

                    if (level + 1) <= 7:
                        _chunk(self.get_comp_doc(i), level + 1)
                    else:
                        _current_doc.append(self.get_comp_doc(i))
                else:
                    _merge_str = "\n\n".join(_current_doc + [self.get_comp_doc(i)])
                    if tokenizer.emb_len(_merge_str) <= self.chunk_size:
                        _current_doc.append(self.get_comp_doc(i))
                    else:
                        _doc.append("\n\n".join(_current_doc))
                        _current_doc = []
                        _current_doc.append(self.get_comp_doc(i))

            _doc.append("\n\n".join(_current_doc))
            _current_doc = []

        _chunk(text, 1)

        return [
            Document(
                page_content=i,
                metadata=dict(token_count=tokenizer.emb_len(i), chunk_index=idx),
            )
            for idx, i in enumerate(_doc)
            if len(i.strip()) > 0
        ]
