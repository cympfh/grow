type Node = File | Directory;

class File {
  kind: "file";
  name: string;
  fullpath: string;
  constructor(path) {
    this.kind = "file";
    this.name = path;
    this.fullpath = path;
  }
}

class Directory {
  kind: "directory";
  name: string;
  nodes: Array<Node>;
  open: boolean;
  constructor(paths: Array<string>) {
    this.kind = "directory";
    this.name = ".";
    this.nodes = paths.map((path) => new File(path));
    this.open = false;
  }
}

export function filetree(paths: Array<string>, slug: string) {
  let d = new Directory(paths);
  d = merge(d);
  open_current(d, slug);
  d.open = true;
  return d;
}

function open_current(d: Directory, slug: string): boolean {
  for (let node of d.nodes) {
    if (node.kind === "directory") {
      let res = open_current(node, slug);
      if (res) {
        d.open = true;
        node.open = true;
        return;
      }
    } else {
      if (node.fullpath == slug) {
        return true;
      }
    }
  }
  return false;
}

function split(name: string): [string, string] {
  if (name.indexOf("/") != -1) {
    let fs = name.split("/");
    return [fs[0], fs.slice(1).join("/")];
  } else {
    return [".", name];
  }
}

function merge(d: Directory): Directory {
  let merged = { ".": [] };
  let keys = ["."];
  for (let node of d.nodes) {
    let [dir, basename] = split(node.name);
    if (!merged[dir]) {
      merged[dir] = [];
      keys.push(dir);
    }
    node.name = basename;
    merged[dir].push(node);
  }
  let nodes = [];
  for (let node of merged["."]) nodes.push(node);
  for (let key of keys) {
    if (key === ".") continue;
    let subdir = new Directory([]);
    subdir.name = key;
    for (let node of merged[key]) {
      subdir.nodes.push(node);
    }
    subdir = merge(subdir);
    nodes.push(subdir);
  }
  let e = new Directory([]);
  e.name = d.name;
  e.nodes = nodes;
  return e;
}
