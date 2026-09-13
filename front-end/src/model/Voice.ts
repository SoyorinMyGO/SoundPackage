export interface Voice {
  id: number;
  remote_id: number;
  name: string;
  alias: string | null;
  length: number;
  used_times: number;
  hash_content: string;
  created_at: string;
  updated_at: string;
}

export interface ImportFileResponse {
  path: string;
  status: string;
  voice: Voice;
  error: string;
}