import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ProjectCard } from '@/components/marketing/project-card';
import { Button } from '@/components/ui/button';
import { featuredProjects } from '@/lib/mock-data';

export function FeaturedProjectsSection() {
  const [hero, ...rest] = featuredProjects.filter((p) => p.featured);

  return (
    <Section dark id="projects">
      <Container>
        <FadeIn>
          <SectionHeader
            eyebrow="Featured work"
            title="Homes that changed"
            description="Real transformations. Real families. Every project tells a story of light reclaimed."
            light
          />
        </FadeIn>

        {hero && (
          <FadeIn>
            <ProjectCard project={hero} variant="featured" />
          </FadeIn>
        )}

        <div className="mt-12 grid gap-10 sm:grid-cols-2 lg:mt-16 lg:gap-12">
          {rest.map((project, i) => (
            <FadeIn key={project.id} delay={i * 0.1}>
              <ProjectCard project={project} />
            </FadeIn>
          ))}
        </div>

        <div className="mt-16 text-center lg:mt-20">
          <Button
            variant="outline"
            size="lg"
            className="border-stone-700 text-stone-100 hover:bg-stone-800"
            asChild
          >
            <Link href="/projects">
              All case studies
              <ArrowUpRight className="ml-1 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </Container>
    </Section>
  );
}
