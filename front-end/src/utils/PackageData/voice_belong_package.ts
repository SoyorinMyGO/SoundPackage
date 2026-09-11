// @ts-ignore
import { remoteApi } from "../../config/axios_config.js";

interface PackageItem{
  id: number
  name: string
  alias: string | null
  isTop: boolean
  voice_list: number[]
  created_at: string
  updated_at: string
}

export async function insert_voice_belong_package(package_list: PackageItem[]): Promise<PackageItem[]> {
    for(const item of package_list) {
        const params = {
            package_id: item.id,
            tag_ids: [],
        }
        console.log('DEBUG(voice_belong_package):params-', params);
        const res = await remoteApi.get("/api/voice/filt", { params });
        console.log('DEBUG(voice_belong_package):语音-语音包关系数据', res.data.data);
        item.voice_list = res.data.data.map((voice: any) => voice.id);
    }
    return package_list;
}