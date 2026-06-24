import { FadeIn } from '@/components/motion/fade-in';
import { Container, Section, SectionHeader } from '@/components/layout/section';
import { ProjectCard } from '@/components/marketing/project-card';
import { Button } from '@/components/ui/button';
import { featuredProjects } from '@/lib/mock-data';
import Link from 'next/link';

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

        <div className="mt-8 grid gap-8 sm:grid-cols-2">
          {rest.map((project, i) => (
            <FadeIn key={project.id} delay={i * 0.1}>
              <ProjectCard project={project} />
            </FadeIn>
          ))}
        </div>

        <div className="mt-12 text-center">
          <Button variant="outline" className="border-stone-700 text-stone-100 hover:bg-stone-800" asChild>
            <Link href="/projects">All projects</Link>
          </Button>
        </div>
      </Container>
    </Section>
  );
}
