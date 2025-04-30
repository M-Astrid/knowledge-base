import os
from abc import abstractmethod
from dataclasses import dataclass, field
from pprint import pprint
from typing import Protocol


DEFAULT_DEPTH = 2

@dataclass
class LeafContent:
    name: str
    dir_path: str
    full_path: str
    depth: int
    children: list["LeafContent"] = field(default_factory=list)


class Leaf(Protocol):
    @abstractmethod
    def get_content(self) -> LeafContent:
        ...


class FileLeaf(Leaf):
    def __init__(self, name, dir_path, parent_depth: int = -1, max_depth: int = 0):
        self.name = name
        self.dir_path = dir_path
        self.depth = parent_depth + 1

    @property
    def full_path(self):
        return f"{self.dir_path}/{self.name}"

    def get_content(self) -> LeafContent:
        return LeafContent(
            name=self.name,
            dir_path=self.dir_path,
            full_path=self.full_path,
            depth=self.depth,
        )


class DirectoryLeaf(Leaf):
    def __init__(self, file_name, dir_path, max_depth: int, parent_depth: int = -1, name: str = None):
        self.name = name or file_name
        self.file_name = file_name
        self.dir_path = dir_path
        self.depth = parent_depth + 1
        self.max_depth = max_depth

    @property
    def full_path(self):
        return f"{self.dir_path}/{self.file_name}"

    @property
    def files(self):
        return os.listdir(self.full_path)

    def get_content(self) -> LeafContent:
        content = LeafContent(
            name=self.file_name,
            dir_path=self.dir_path,
            full_path=self.full_path,
            depth=self.depth,
        )
        if self.depth == self.max_depth:
            return content

        for file in self.files:
            if os.path.isdir(f"{self.full_path}/{file}"):
                leaf_content = DirectoryLeaf(file, self.full_path, self.max_depth, self.depth).get_content()
            else:
                leaf_content = FileLeaf(file, self.full_path, self.max_depth, self.depth).get_content()
            content.children.append(leaf_content)
        return content


class Project:
    def __init__(self, dir_path: str, max_depth: int, name: str = None, skip_first: bool = False):
        self.name = name or dir_path
        self.dir_path = dir_path
        self.max_depth = max_depth
        self.skip_first = skip_first

    def get_content(self) -> LeafContent:
        project = DirectoryLeaf(self.dir_path, ".", max_depth=depth)
        return project.get_content()


class Renderer(Protocol):
    @abstractmethod
    def __call__(self, tree: LeafContent, depth: int = DEFAULT_DEPTH, **kwargs):
        ...


class MDRenderer(Renderer):
    ident: str = "  "
    prefix_template: str = "{ident}{char} "
    link_template: str = "[{name}]({link})"
    base_template: str = "{name}"
    dir_char = "-"
    file_char = "-"
    end_char = "  \n"
    output = ""


    def __call__(self, content: LeafContent, is_links: bool = False, **kwargs):
        self.output += self.prefix_template.format(char=self.file_char, ident=self.ident * content.depth)
        if is_links:
            self.output += self.link_template.format(name=content.name, link=content.full_path)
        else:
            self.output += self.base_template.format(name=content.name)

        self.output += self.end_char

        for child in content.children:
            self(child, is_links=is_links)

        return self.output


class HTMLRenderer(Renderer):
    def __call__(self, leaf: Leaf, **kwargs):
        raise NotImplementedError



class TextRenderer(Renderer):
    prefix_template: str = "{'  '*depth}{char} "

    def __call__(self, leaf: Leaf, **kwargs):
        # content = leaf.get_content()
        # output = self.prefix_template.format(char="└─" if content.depth == 0 else "├─", depth=content.depth)
        raise NotImplementedError


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cute directory tree generator.")

    parser.add_argument('--format', type=str, default='md', choices=['md', 'txt'], help="Формат вывода: текст или markdown.")
    parser.add_argument('--depth', type=int, default=DEFAULT_DEPTH, help="Максимальная глубина обхода.")
    parser.add_argument('--output', type=str, default="output.txt", help="Имя файла для вывода результата.")

    args = parser.parse_known_args()[0]

    depth, format_ = args.depth, args.format

    render = MDRenderer() if format_ == 'md' else TextRenderer()
    project = Project("knowledge_base", max_depth=depth)
    tree = project.get_content()

    formatted = render(tree, is_links=True, depth=depth)

    # if args.output:
    with open(args.output, 'w') as f:
        f.write(formatted)
    # else:
    #     print(formatted)
