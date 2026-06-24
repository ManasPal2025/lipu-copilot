/**
 * Local architecture photography — served from /public/images.
 * Run scripts/download-images.ps1 to re-fetch assets if needed.
 * Selection rules: see image-guidelines.md (Odisha / Indian architecture only).
 */

export interface ImageAsset {
  src: string;
  alt: string;
}

const local = (path: string, alt: string): ImageAsset => ({
  src: `/images/${path}`,
  alt,
});

export const images = {
  hero: local(
    'hero/main.jpg',
    'Modern high-rise apartment in Bengaluru with floor-to-ceiling glazing and warm evening light',
  ),

  transformation: local(
    'hero/transformation.jpg',
    'Indian apartment living room flooded with natural daylight through panoramic windows',
  ),

  editorialStrip: local(
    'hero/editorial-strip.jpg',
    'Multi-story residential building in Bengaluru with refined architectural symmetry at dusk',
  ),

  projects: {
    coastalResidence: local(
      'projects/coastal-residence.jpg',
      'Coastal apartment in Puri with balcony glazing and tropical greenery framing the sea breeze',
    ),
    skylinePenthouse: local(
      'projects/skyline-penthouse.jpg',
      'High-rise residential tower in Bhubaneswar with contemporary balcony glazing',
    ),
    heritageRevival: local(
      'projects/heritage-revival.jpg',
      'Heritage residential building in Cuttack with restored facade and classical Indian proportions',
    ),
    lonavalaRetreat: local(
      'projects/lonavala-retreat.jpg',
      'Modern Odisha villa with expansive glazing opening to forested hillside views',
    ),
    goaVilla: local(
      'projects/goa-villa.jpg',
      'Premium duplex villa near Puri with large glass openings and tropical courtyard',
    ),
    corporateLobby: local(
      'projects/corporate-lobby.jpg',
      'Commercial glass facade on an Indian office building — structural glazing entrance',
    ),
  },

  beforeAfter: {
    bandraBefore: local(
      'before-after/bandra-before.jpg',
      'Traditional Indian duplex exterior before window transformation',
    ),
    bandraAfter: local(
      'before-after/bandra-after.jpg',
      'Upgraded Indian apartment with refined UPVC glazing and improved daylight',
    ),
    lonavalaBefore: local(
      'before-after/lonavala-before.jpg',
      'Modest Indian hillside home with small windows before renovation',
    ),
    lonavalaAfter: local(
      'before-after/lonavala-after.jpg',
      'Transformed Indian home interior with expansive glazing and forest views',
    ),
    puneBefore: local(
      'before-after/pune-before.jpg',
      'Heritage-era Indian home exterior with original timber frames',
    ),
    puneAfter: local(
      'before-after/pune-after.jpg',
      'Restored heritage interior with period-accurate windows and warm Odisha light',
    ),
  },

  designStyles: {
    modernMinimal: local(
      'design/modern-minimal.jpg',
      'Minimal modern Indian apartment interior with floor-to-ceiling glass',
    ),
    europeanClassic: local(
      'design/european-classic.jpg',
      'Symmetrical Indian residential facade with refined window proportions',
    ),
    coastalResilient: local(
      'design/coastal-resilient.jpg',
      'Coastal Indian apartment with weather-resistant glazing facing the sea',
    ),
    tropicalOpen: local(
      'design/tropical-open.jpg',
      'Tropical Odisha villa with open-plan living connected to garden terrace',
    ),
  },

  products: {
    horizonSliding: local(
      'products/horizon-sliding.jpg',
      'Ultra-slim sliding window system on an Indian high-rise facade',
    ),
    horizonDetail: local(
      'products/horizon-detail.jpg',
      'Sliding window hardware and seal detail close-up',
    ),
    atelierCasement: local(
      'products/atelier-casement.jpg',
      'Casement window with concealed hinge on an Indian residential facade',
    ),
    atelierDetail: local('products/atelier-detail.jpg', 'Window handle and multi-point locking detail'),
    grandEntrance: local(
      'products/grand-entrance.jpg',
      'Grand entrance door with premium hardware in an Indian luxury foyer',
    ),
    grandDetail: local('products/grand-detail.jpg', 'Entrance door threshold and thermal break detail'),
    gardenPortal: local(
      'products/garden-portal.jpg',
      'Floor-to-ceiling sliding doors opening to an Indian villa terrace',
    ),
    gardenDetail: local('products/garden-detail.jpg', 'Sliding door track and flush threshold detail'),
    facadeSystem: local(
      'products/facade-system.jpg',
      'Commercial facade with structural glazing on an Indian office tower',
    ),
    facadeDetail: local(
      'products/facade-detail.jpg',
      'Curtain wall glazing node on an Indian commercial building',
    ),
    skylineFixed: local(
      'products/skyline-fixed.jpg',
      'Panoramic fixed window with city views from an Indian high-rise',
    ),
    skylineDetail: local('products/skyline-detail.jpg', 'Fixed picture window sightline and glass edge detail'),
  },

  gallery: {
    morningLight: local(
      'gallery/morning-light.jpg',
      'Sunlit Indian living room with soft morning shadows through glass',
    ),
    gardenPortal: local(
      'gallery/garden-portal.jpg',
      'Sliding garden doors opening to a serene Indian courtyard',
    ),
    urbanEdge: local(
      'gallery/urban-edge.jpg',
      'Indian high-rise facade with precision glazing grid — Kolkata skyline',
    ),
    monsoonCalm: local(
      'gallery/monsoon-calm.jpg',
      'Indian residential glass facade during monsoon season',
    ),
    courtyardFrame: local(
      'gallery/courtyard-frame.jpg',
      'Internal courtyard framed by windows on an Indian duplex',
    ),
    duskSilhouette: local(
      'gallery/dusk-silhouette.jpg',
      'Indian home at dusk with warm interior glow visible through glass',
    ),
    profileDetail: local(
      'gallery/profile-detail.jpg',
      'UPVC window profile cross-section showing engineering precision',
    ),
    stairwellLight: local(
      'gallery/stairwell-light.jpg',
      'Indian duplex stairwell with vertical glazing shaft bringing natural light',
    ),
    seaHorizon: local(
      'gallery/sea-horizon.jpg',
      'Coastal Puri apartment with Bay of Bengal views through panoramic glass',
    ),
    minimalBedroom: local(
      'gallery/minimal-bedroom.jpg',
      'Minimal bedroom in an Indian apartment with floor-to-ceiling glazing',
    ),
    villaPool: local(
      'gallery/villa-pool.jpg',
      'Premium Odisha villa poolside with sliding glass walls',
    ),
    cityPenthouse: local(
      'gallery/city-penthouse.jpg',
      'Indian residential towers at dusk — urban apartment living',
    ),
  },

  about: {
    craft: local('about/craft.jpg', 'UPVC window profile and material quality — engineering craft detail'),
    studio: local('about/studio.jpg', 'LIPU design studio with architectural models and natural light'),
    manifesto: local(
      'about/manifesto.jpg',
      'Premium Indian residence embodying the transformation philosophy',
    ),
  },

  team: {
    aditya: local('team/aditya.jpg', 'Aditya Rao — design director portrait'),
    meera: local('team/meera.jpg', 'Meera Iyer — head of projects portrait'),
    rohan: local('team/rohan.jpg', 'Rohan Patel — technical director portrait'),
  },

  contact: local(
    'contact/exterior.jpg',
    'Modern Indian duplex exterior — inspiration for your Odisha home transformation',
  ),

  visualizer: local(
    'contact/visualizer.jpg',
    'Premium Indian duplex facade ideal for AI visualization preview',
  ),

  quoteCta: local('hero/main.jpg', 'Premium Indian apartment at golden hour'),

  pageHero: {
    projects: local('page-heroes/projects.jpg', 'Indian villa case study — modern residence with glazing'),
    products: local('page-heroes/products.jpg', 'Premium UPVC window system on an Indian home'),
    gallery: local('page-heroes/gallery.jpg', 'Real Indian living room inspiration with natural light through UPVC windows'),
    about: local('page-heroes/about.jpg', 'Craftsmanship and design studio atmosphere'),
    contact: local('page-heroes/contact.jpg', 'Inviting Indian home — begin your transformation in Odisha'),
  },
} as const;

export type AspectRatio = 'video' | 'square' | 'portrait' | 'wide' | 'hero' | 'auto';

export const aspectClasses: Record<AspectRatio, string> = {
  video: 'aspect-video',
  square: 'aspect-square',
  portrait: 'aspect-[3/4]',
  wide: 'aspect-[21/9]',
  hero: 'aspect-[4/5] sm:aspect-[16/9] lg:aspect-[21/9]',
  auto: '',
};
