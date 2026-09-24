export interface PackageItem {
  id: number
  name: string
  alias: string | null
  isTop: boolean
  voice_list: number[] | null
  created_at: string
  updated_at: string
}

export interface PackageInfo {
  id: number;
  name: string;
}