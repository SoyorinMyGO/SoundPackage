export interface Voice {
  id: number;
  name: string;
  alias: string | null;
  length: number;
  used_times: number;
  created_at: string;
  updated_at: string;
}