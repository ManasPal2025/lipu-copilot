import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { ImagePlaceholder } from '@/components/layout/section';
import type { Project } from '@/lib/mock-data';

interface ProjectCardProps {
  project: Project;
  variant?: 'featured' | 'compact';
}

export function ProjectCard({ project, variant = 'compact' }: ProjectCardProps) {
  if (variant === 'featured') {
    return (
      <Link href="/projects" className="group block">
        <div className="relative overflow-hidden">
          <ImagePlaceholder label={project.imageLabel} aspect="wide" />
          <div className="absolute inset-0 bg-gradient-to-t from-stone-925/90 via-stone-925/20 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-6 sm:p-10 lg:p-14">
            <p className="text-xs uppercase tracking-[0.2em] text-stone-400">
              {project.location} · {project.type}
            </p>
            <h3 className="mt-2 font-display text-3xl text-stone-50 sm:text-4xl lg:text-5xl">{project.title}</h3>
            <p className="mt-4 max-w-2xl text-stone-300">{project.description}</p>
            <span className="mt-6 inline-flex items-center gap-2 text-sm text-stone-200 group-hover:text-white">
              View project
              <ArrowUpRight className="h-4 w-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            </span>
          </div>
        </div>
      </Link>
    );
  }

  return (
    <Link href="/projects" className="group block">
      <ImagePlaceholder label={project.imageLabel} aspect="video" />
      <div className="mt-4 flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">{project.location}</p>
          <h3 className="mt-1 font-display text-2xl group-hover:text-accent">{project.title}</h3>
          <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">{project.description}</p>
        </div>
        <ArrowUpRight className="mt-1 h-5 w-5 shrink-0 text-muted-foreground transition-transform group-hover:text-foreground group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
      </div>
    </Link>
  );
}
