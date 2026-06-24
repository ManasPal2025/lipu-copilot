'use client';

import { MapPin } from 'lucide-react';

import { useCity } from '@/components/providers/city-provider';
import { getSupportedCities, type CityId } from '@/lib/city-style';
import { cn } from '@/lib/utils';

interface CitySelectorProps {
  inverted?: boolean;
  className?: string;
}

export function CitySelector({ inverted = false, className }: CitySelectorProps) {
  const { cityId, setCityId } = useCity();
  const cities = getSupportedCities();

  return (
    <label
      className={cn(
        'inline-flex items-center gap-1.5 rounded-sm border px-2 py-1.5 text-xs',
        inverted
          ? 'border-stone-600/50 bg-stone-925/30 text-stone-200'
          : 'border-border bg-background text-foreground',
        className,
      )}
    >
      <MapPin className="h-3.5 w-3.5 shrink-0 opacity-70" aria-hidden />
      <span className="sr-only">Select your city</span>
      <select
        value={cityId}
        onChange={(e) => setCityId(e.target.value as CityId)}
        className={cn(
          'max-w-[7.5rem] cursor-pointer appearance-none bg-transparent pr-1 text-xs font-medium outline-none sm:max-w-[9rem]',
          inverted ? 'text-stone-100' : 'text-foreground',
        )}
        aria-label="Select city for localized imagery"
      >
        {cities.map((city) => (
          <option key={city.id} value={city.id}>
            {city.label}
          </option>
        ))}
      </select>
    </label>
  );
}
