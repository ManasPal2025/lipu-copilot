'use client';

import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { ImageZoom } from '@/components/motion/image-zoom';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import type { Project } from '@/lib/mock-data';

interface ProjectCardProps {
  project: Project;
  variant?: 'featured' | 'compact' | 'editorial';
}

export function ProjectCard({ project, variant = 'compact' }: ProjectCardProps) {
  if (variant === 'featured') {
    return (
      <Link href="/projects" className="group block">
        <ImageZoom className="relative">
          <div className="relative min-h-[480px] sm:min-h-[560px] lg:min-h-[640px]">
            <ArchitecturalImage
              src={project.image.src}
              alt={project.image.alt}
              aspect="auto"
              containerClassName="absolute inset-0 h-full w-full"
              sizes="100vw"
              priority
            />
            <div className="absolute inset-0 bg-gradient-to-t from-stone-925/95 via-stone-925/30 to-stone-925/10" />
            <div className="absolute bottom-0 left-0 right-0 p-8 sm:p-12 lg:p-16">
              <p className="text-xs uppercase tracking-[0.25em] text-stone-400">
                {project.location} · {project.type}
              </p>
              <h3 className="mt-3 font-display text-4xl text-stone-50 sm:text-5xl lg:text-6xl">
                {project.title}
              </h3>
              <p className="mt-5 max-w-2xl text-base leading-relaxed text-stone-300/90 editorial-prose sm:text-lg">
                {project.description}
              </p>
              {project.pullQuote && (
                <p className="mt-6 border-l border-stone-600 pl-4 font-display text-lg text-stone-300/90 italic">
                  {project.pullQuote}
                </p>
              )}
              <span className="mt-8 inline-flex items-center gap-2 text-sm tracking-wide text-stone-200 transition-colors group-hover:text-white">
                Read case study
                <ArrowUpRight className="h-4 w-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
              </span>
            </div>
          </div>
        </ImageZoom>
      </Link>
    );
  }

  if (variant === 'editorial') {
    return (
      <article className="group">
        <ImageZoom>
          <ArchitecturalImage
            src={project.image.src}
            alt={project.image.alt}
            aspect="wide"
            sizes="(max-width: 1024px) 100vw, 58vw"
          />
        </ImageZoom>
        <div className="mt-8 lg:mt-10">
          <p className="text-xs uppercase tracking-[0.2em] text-stone-500">
            {project.location} · {project.type}
          </p>
          <h2 className="mt-3 font-display text-3xl text-stone-50 sm:text-4xl lg:text-5xl">{project.title}</h2>
          <p className="mt-4 max-w-xl leading-relaxed text-stone-400 editorial-prose">{project.description}</p>
        </div>
      </article>
    );
  }

  return (
    <Link href="/projects" className="group block">
      <ImageZoom>
        <ArchitecturalImage
          src={project.image.src}
          alt={project.image.alt}
          aspect="video"
          sizes="(max-width: 768px) 100vw, 50vw"
        />
      </ImageZoom>
      <div className="mt-5 flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.15em] text-muted-foreground">{project.location}</p>
          <h3 className="mt-2 font-display text-2xl transition-colors group-hover:text-accent">{project.title}</h3>
          <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-muted-foreground">{project.description}</p>
        </div>
        <ArrowUpRight className="mt-1 h-5 w-5 shrink-0 text-muted-foreground transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:text-foreground" />
      </div>
    </Link>
  );
}
