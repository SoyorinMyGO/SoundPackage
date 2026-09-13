// 响应式缓存
import {onScopeDispose, ref, watch} from "vue";
import {getLocalStorage, setLocalStorage} from "./local_storage";

export function useLocalStorage<T>(key: string, initialValue: T) {
    const data = ref<T>(getLocalStorage<T>(key) ?? initialValue);

    const syncFromStorage = (event?: CustomEvent<{ key: string; value: T }>) => {
        const storageKey = event?.detail?.key ?? key;
        if (storageKey !== key) return;

        const nextValue = event?.detail?.value ?? getLocalStorage<T>(key) ?? initialValue;
        data.value = nextValue;
    };

    watch(data, (newVal) => {
        setLocalStorage(key, newVal);
    }, { deep: true });

    if (typeof window !== 'undefined') {
        const handler = ((event: Event) => {
            const customEvent = event as CustomEvent<{ key: string; value: T }>;
            syncFromStorage(customEvent);
        }) as EventListener;

        window.addEventListener('local-storage-change', handler);
        onScopeDispose(() => {
            window.removeEventListener('local-storage-change', handler);
        });
    }

    return data;
}