
export const categories = [
  {
    name: "Development",
    slug: "development",
    description:
      "Learning Python, solving problems, and documenting the journey.",
    icon: "⌘",
  },
  {
    name: "Projects",
    slug: "projects",
    description:
      "Building tools, experimenting with technology, and sharing results.",
    icon: "◈",
  },
  {
    name: "Life",
    slug: "life",
    description:
      "Thoughts, experiences, and lessons beyond the keyboard.",
    icon: "✎",
  },
] as const;

export function getCategoryUrl(slug: string) {
  return `/blog/category/${slug}/`;
}

