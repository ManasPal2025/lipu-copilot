'use client';

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';

import {
  getCityImage,
  getCityStyle,
  getDefaultCityId,
  normalizeCityId,
  readStoredCityId,
  writeStoredCityId,
  type CityId,
  type CityStyle,
  type ImageCategory,
} from '@/lib/city-style';
import type { ImageAsset } from '@/lib/images';

interface CityContextValue {
  cityId: CityId;
  cityLabel: string;
  style: CityStyle;
  setCityId: (id: CityId) => void;
  getImage: (category: ImageCategory) => ImageAsset;
}

const CityContext = createContext<CityContextValue | null>(null);

export function CityProvider({ children }: { children: ReactNode }) {
  const [cityId, setCityIdState] = useState<CityId>(getDefaultCityId());
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const stored = readStoredCityId();
    if (stored) setCityIdState(stored);
    setHydrated(true);
  }, []);

  const setCityId = useCallback((id: CityId) => {
    const normalized = normalizeCityId(id);
    setCityIdState(normalized);
    writeStoredCityId(normalized);
  }, []);

  const style = getCityStyle(cityId);

  const value = useMemo<CityContextValue>(
    () => ({
      cityId,
      cityLabel: style.label,
      style,
      setCityId,
      getImage: (category: ImageCategory) => getCityImage(cityId, category),
    }),
    [cityId, setCityId, style],
  );

  if (!hydrated) {
    return <CityContext.Provider value={value}>{children}</CityContext.Provider>;
  }

  return <CityContext.Provider value={value}>{children}</CityContext.Provider>;
}

export function useCity(): CityContextValue {
  const ctx = useContext(CityContext);
  if (!ctx) {
    throw new Error('useCity must be used within CityProvider');
  }
  return ctx;
}
