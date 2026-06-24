'use client';

import { useMemo, useState } from 'react';

import { FadeIn } from '@/components/motion/fade-in';
import { ImageZoom } from '@/components/motion/image-zoom';
import { ArchitecturalImage } from '@/components/ui/architectural-image';
import {
  inspirationCategories,
  type GalleryInspirationItem,
} from '@/lib/gallery-inspiration';
import { cn } from '@/lib/utils';

interface GalleryGridProps {
  items: GalleryInspirationItem[];
}

export function GalleryGrid({ items }: GalleryGridProps) {
  const [activeSlug, setActiveSlug] = useState<string | null>(null);

  const filteredCategories = useMemo(() => {
    if (!activeSlug) return inspirationCategories;
    return inspirationCategories.filter((c) => c.slug === activeSlug);
  }, [activeSlug]);

  const itemsByCategory = useMemo(() => {
    const map = new Map<string, GalleryInspirationItem[]>();
    for (const item of items) {
      const list = map.get(item.categorySlug) ?? [];
      list.push(item);
      map.set(item.categorySlug, list);
    }
    return map;
  }, [items]);

  return (
    <>
      <FadeIn>
        <div className="mb-14 flex flex-wrap justify-center gap-2">
          <button
            type="button"
            onClick={() => setActiveSlug(null)}
            className={cn(
              'rounded-full border px-4 py-1.5 text-xs uppercase tracking-wider transition-colors',
              !activeSlug
                ? 'border-foreground bg-foreground text-background'
                : 'border-border text-muted-foreground hover:border-foreground/40',
            )}
          >
            All ideas
          </button>
          {inspirationCategories.map((cat) => (
            <button
              key={cat.slug}
              type="button"
              onClick={() => setActiveSlug(cat.slug)}
              className={cn(
                'rounded-full border px-4 py-1.5 text-xs uppercase tracking-wider transition-colors',
                activeSlug === cat.slug
                  ? 'border-foreground bg-foreground text-background'
                  : 'border-border text-muted-foreground hover:border-foreground/40',
              )}
            >
              {cat.title}
            </button>
          ))}
        </div>
      </FadeIn>

      <div className="space-y-20 lg:space-y-28">
        {filteredCategories.map((category, catIndex) => {
          const categoryItems = itemsByCategory.get(category.slug) ?? [];
          return (
            <FadeIn key={category.slug} delay={catIndex * 0.04}>
              <section id={category.slug} className="scroll-mt-28">
                <div className="mb-10 max-w-3xl">
                  <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                    {category.subtitle} · 10 photos
                  </p>
                  <h2 className="mt-3 font-display text-3xl sm:text-4xl lg:text-5xl">{category.title}</h2>
                  <p className="mt-4 leading-relaxed text-muted-foreground editorial-prose">
                    {category.description}
                  </p>
                </div>

                <div className="columns-1 gap-6 sm:columns-2 lg:columns-3 lg:gap-8">
                  {categoryItems.map((item) => (
                    <figure key={item.id} className="group relative mb-6 break-inside-avoid lg:mb-8">
                      <div className="relative overflow-hidden">
                        <ImageZoom>
                          <ArchitecturalImage
                            src={item.image.src}
                            alt={item.image.alt}
                            aspect={
                              item.span === 'tall' ? 'portrait' : item.span === 'wide' ? 'wide' : 'video'
                            }
                            containerClassName={cn(item.span === 'tall' && 'min-h-[420px]')}
                            sizes="(max-width: 768px) 100vw, 33vw"
                          />
                        </ImageZoom>
                        <div className="absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-stone-925/85 via-stone-925/25 to-transparent p-6 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
                          <span className="font-display text-lg text-stone-50">{item.title}</span>
                          <p className="mt-1 text-xs uppercase tracking-wider text-stone-400">
                            {item.location} · {item.category}
                          </p>
                        </div>
                      </div>
                      <figcaption className="mt-3 px-1 sm:hidden">
                        <span className="font-display text-base">{item.title}</span>
                        <p className="text-xs text-muted-foreground">{item.location}</p>
                      </figcaption>
                    </figure>
                  ))}
                </div>
              </section>
            </FadeIn>
          );
        })}
      </div>
    </>
  );
}
