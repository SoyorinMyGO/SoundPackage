// 响应式缓存
import {ref, watch} from "vue";
import {getLocalStorage, setLocalStorage} from "./local_storage";

export function useLocalStorage<T>(key: string, initialValue: T) {
    const data = ref<T>(getLocalStorage(key) ?? initialValue);

    watch(data, (newVal) => {
        setLocalStorage(key, newVal);
    }, { deep: true });

    return data
}