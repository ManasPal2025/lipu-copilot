// API Response Types
export interface ApiResponse<T> {
  status: 'success' | 'error';
  code: number;
  data?: T;
  error?: {
    type: string;
    message: string;
    details?: Record<string, any>;
  };
  meta: {
    timestamp: string;
    request_id: string;
    version: string;
  };
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_count: number;
  total_pages: number;
  has_next: boolean;
  has_previous: boolean;
}

// Add more type exports as needed
