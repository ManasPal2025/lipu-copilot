import { images, type ImageAsset } from '@/lib/images';

/**
 * Structured inputs for the future transformation service.
 * Do not collect free-form AI prompts from the user.
 */
export type TransformTarget = 'windows' | 'doors' | 'balcony' | 'terrace' | 'outdoor';

export type TransformVariant = 'sliding' | 'casement' | 'large-opening' | 'bifold' | 'french';

export type TransformPhase = 'empty' | 'uploaded' | 'configured' | 'processing' | 'result' | 'error';

export interface TransformRequest {
  target: TransformTarget;
  variant?: TransformVariant;
  sourceKind: 'upload' | 'sample';
  sampleId?: string;
}

export interface TransformDemoResult {
  image: ImageAsset;
  label: string;
}

const POSSIBILITY_BY_TARGET: Record<TransformTarget, ImageAsset> = {
  windows: images.ecotechTransform.living,
  doors: images.ecotechTransform.living,
  balcony: images.ecotechTransform.balcony,
  terrace: images.ecotechTransform.living,
  outdoor: images.ecotechTransform.villaAlt,
};

/**
 * Demonstration mapping only.
 * Replace this function with the future transformation service:
 * Visualize My Space → transformation service → generated result.
 */
export function getDemoResult(request: TransformRequest, currentSrc?: string): TransformDemoResult {
  let image = POSSIBILITY_BY_TARGET[request.target];

  if (currentSrc && image.src === currentSrc) {
    image =
      request.target === 'outdoor' || request.target === 'terrace'
        ? images.ecotechTransform.living
        : images.ecotechTransform.villaAlt;
  }

  return {
    image,
    label: 'Ecotech possibility',
  };
}
