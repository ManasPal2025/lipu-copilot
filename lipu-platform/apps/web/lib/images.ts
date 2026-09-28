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

  ecotechProducts: {
    hero: local(
      'products/ecotech/product-hero-01.png',
      'Living space with large-format glazing opening to landscape',
    ),
    slidingWindow: local(
      'products/ecotech/product-sliding-window-01.png',
      'Sliding window in a residential interior',
    ),
    casementWindow: local(
      'products/ecotech/product-casement-window-01.png',
      'Casement window opening toward a garden view',
    ),
    fixedWindow: local(
      'products/ecotech/product-fixed-window-01.png',
      'Fixed picture window with panoramic outlook',
    ),
    tiltTurn: local(
      'products/ecotech/product-tilt-turn-01.png',
      'Tilt and turn window in a bedroom setting',
    ),
    combinationWindow: local(
      'products/ecotech/product-combination-window-01.png',
      'Combination window with mixed fixed and operable panels',
    ),
    slidingDoor: local(
      'products/ecotech/product-sliding-door-01.png',
      'Sliding door connecting a living room to outdoor space',
    ),
    frenchDoor: local(
      'products/ecotech/product-french-door-01.png',
      'French doors opening toward a terrace',
    ),
    casementDoor: local(
      'products/ecotech/product-casement-door-01.png',
      'Casement door in a residential opening',
    ),
    bifoldDoor: local(
      'products/ecotech/product-bifold-door-01.png',
      'Bifold doors opening toward a garden',
    ),
    largeFormat: local(
      'products/ecotech/product-lift-slide-01.png',
      'Large-format glazed opening in a modern residence',
    ),
    cornerGlazing: local(
      'products/ecotech/product-corner-glazing-01.png',
      'Corner glazing integrated into a contemporary villa',
    ),
    balconySystem: local(
      'products/ecotech/product-balcony-system-01.png',
      'Balcony glazing system enclosing an outdoor space',
    ),
    partition: local(
      'products/ecotech/product-partition-system-01.png',
      'Interior glass partition in a contemporary space',
    ),
    customOpening: local(
      'products/ecotech/product-custom-opening-01.png',
      'Custom architectural opening in a modern home',
    ),
    hardwareDetail: local(
      'products/ecotech/product-hardware-detail-01.png',
      'Window hardware detail',
    ),
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

  ecotechInspiration: {
    hero: local(
      'inspiration/ecotech/inspiration-living-01.png',
      'Living space opening through large glazing toward the landscape',
    ),
    living1: local('inspiration/ecotech/inspiration-living-01.png', 'Light across a living space'),
    living2: local('inspiration/ecotech/inspiration-living-02.png', 'Living space with a glazed garden outlook'),
    living3: local('inspiration/ecotech/inspiration-living-03.png', 'Open living room with garden outlook'),
    living4: local('inspiration/ecotech/inspiration-living-04.png', 'Living interior framed by glass'),
    bedroom1: local('inspiration/ecotech/inspiration-bedroom-01.png', 'Calm, light-filled bedroom'),
    bedroom2: local('inspiration/ecotech/inspiration-bedroom-02.png', 'Private bedroom with a quiet view'),
    bedroom3: local('inspiration/ecotech/inspiration-bedroom-03.png', 'Bedroom opening toward morning light'),
    balcony1: local('inspiration/ecotech/inspiration-balcony-01.png', 'Balcony as an extension of the room'),
    balcony2: local('inspiration/ecotech/inspiration-balcony-02.png', 'Compact balcony, made usable'),
    balcony3: local('inspiration/ecotech/inspiration-balcony-03.png', 'Framing the view from a balcony'),
    balcony4: local('inspiration/ecotech/inspiration-balcony-04.png', 'Balcony lounge in natural light'),
    terrace1: local('inspiration/ecotech/inspiration-terrace-01.png', 'Terrace living, open to the air'),
    terrace2: local('inspiration/ecotech/inspiration-terrace-02.png', 'An extension of the terrace'),
    terrace3: local('inspiration/ecotech/inspiration-terrace-03.png', 'Terrace space at dusk'),
    terrace4: local('inspiration/ecotech/inspiration-terrace-04.png', 'Indoor–outdoor terrace threshold'),
    outdoor1: local('inspiration/ecotech/inspiration-outdoor-01.png', 'Outdoor living under open sky'),
    outdoor2: local('inspiration/ecotech/inspiration-outdoor-02.png', 'Garden and landscape, held by glass'),
    villa1: local('inspiration/ecotech/inspiration-residential-01.png', 'Villa openings, generous and still'),
    villa2: local('inspiration/ecotech/inspiration-residential-02.png', 'Residential architecture in evening light'),
    commercial: local(
      'inspiration/ecotech/inspiration-commercial-01.png',
      'Contemporary commercial interior with glazing',
    ),
  },

  ecotechGallery: {
    hero: local(
      'gallery/ecotech/gallery-apartment-01.png',
      'Apartment living room with floor-to-ceiling glazing and a city outlook',
    ),
    villa: local(
      'gallery/ecotech/gallery-villa-01.png',
      'Villa at dusk with large glazed openings reflected in a still pool',
    ),
    residential: local(
      'gallery/ecotech/gallery-residential-01.png',
      'Residential opening with folding glass doors to the terrace',
    ),
    apartment: local(
      'gallery/ecotech/gallery-apartment-01.png',
      'Apartment interior with sliding glass and a bright outlook',
    ),
    balcony: local(
      'gallery/ecotech/gallery-balcony-01.png',
      'Balcony living with glazed enclosure and planted outlook',
    ),
    commercial: local(
      'gallery/ecotech/gallery-commercial-01.png',
      'Commercial interior with architectural glazing',
    ),
    hospitality: local(
      'gallery/ecotech/gallery-hospitality-01.png',
      'Hospitality interior shaped by glass and natural light',
    ),
  },

  ecotechTransform: {
    hero: local(
      'transform/ecotech/transform-sample-living-01.png',
      'Living space opening through sliding glass to a terrace and landscape',
    ),
    living: local(
      'transform/ecotech/transform-sample-living-01.png',
      'Living interior with large sliding doors to an outdoor terrace',
    ),
    balcony: local(
      'transform/ecotech/transform-sample-balcony-01.png',
      'Balcony with glazed openings and a planted outlook',
    ),
    apartment: local(
      'transform/ecotech/transform-sample-apartment-01.png',
      'Apartment facade with windows, doors, and balcony openings',
    ),
    villa: local(
      'transform/ecotech/transform-sample-villa-01.png',
      'Villa with architectural windows, doors, and balcony openings',
    ),
    villaAlt: local(
      'transform/ecotech/transform-sample-villa-02.png',
      'Contemporary villa with glazed balconies and warm timber openings',
    ),
  },

  ecotechHome: {
    hero: local(
      'home/ecotech/home-hero-01.png',
      'Architectural living space with floor-to-ceiling glazing',
    ),
    living: local('home/ecotech/home-living-01.png', 'Living space with large glazed openings'),
    bedroom: local('home/ecotech/home-bedroom-01.png', 'Bedroom with refined window light'),
    balcony: local('home/ecotech/home-balcony-01.png', 'Balcony opening with glazed enclosure'),
    indoorOutdoor: local(
      'home/ecotech/home-indoor-outdoor-01.png',
      'Indoor–outdoor living through wide glazed doors',
    ),
    villa: local('home/ecotech/home-villa-exterior-01.png', 'Villa exterior with architectural openings'),
    productDetail: local(
      'home/ecotech/home-product-detail-01.png',
      'Close view of a window or door system in a home',
    ),
    transformBefore: local(
      'home/ecotech/home-transform-before-01.png',
      'Home facade before window and door upgrade',
    ),
    transformAfter: local(
      'home/ecotech/home-transform-after-01.png',
      'The same home facade after Ecotech openings',
    ),
    cta: local('home/ecotech/home-cta-01.png', 'Architectural interior for consultation'),
  },

  ecotechServices: {
    hero: local(
      'services/ecotech/services-hero-01.png',
      'Architectural residence with expansive glazing',
    ),
    windowsDoors: local(
      'services/ecotech/services-windows-doors-01.png',
      'Windows and doors as the foundation of a space',
    ),
    balcony: local('services/ecotech/services-balcony-01.png', 'Balcony transformation with glazing'),
    terrace: local('services/ecotech/services-terrace-01.png', 'Terrace environment with glazed openings'),
    sunroom: local('services/ecotech/services-sunroom-01.png', 'Sunroom with expansive glass walls'),
    gardenRoom: local('services/ecotech/services-garden-room-01.png', 'Garden room opening to planted space'),
    gazebo: local('services/ecotech/services-gazebo-01.png', 'Gazebo with refined framing'),
    outdoorLiving: local(
      'services/ecotech/services-outdoor-living-01.png',
      'Outdoor living defined by large openings',
    ),
    poolside: local('services/ecotech/services-poolside-01.png', 'Poolside space with architectural glazing'),
    commercialOffice: local(
      'services/ecotech/services-commercial-office-01.png',
      'Commercial office interior with contemporary glazing',
    ),
    salon: local('services/ecotech/services-salon-01.png', 'Salon interior with glass and light'),
    cafeRestaurant: local(
      'services/ecotech/services-cafe-restaurant-01.png',
      'Café or restaurant interior with large openings',
    ),
    hospitality: local(
      'services/ecotech/services-hospitality-01.png',
      'Hospitality environment with architectural glazing',
    ),
  },

  ecotechContact: {
    hero: local('contact/ecotech/contact-hero-01.png', 'Architectural interior introducing Ecotech contact'),
    consultation: local(
      'contact/ecotech/contact-consultation-01.png',
      'Consultation setting with contemporary openings',
    ),
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
