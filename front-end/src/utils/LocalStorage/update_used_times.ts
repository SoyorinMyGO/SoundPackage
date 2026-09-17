import {Voice} from "../../model/Voice";
import {ref, Ref} from "vue";
import {useLocalStorage} from "./use_storage";

const voiceInfo: Ref<Record<string, object>> = useLocalStorage('vocie_info', {});

export function updateUsedTimes(item: Voice): void{
    console.log(`DEBUG(used_times): ${item.name}次数++`)
    item.used_times++;
    voiceInfo[item.hash_content] = item;
    // 若当前语音在网络有资源,向网络发送更新请求
    if (item.remote_id !== 0) {

    }
}