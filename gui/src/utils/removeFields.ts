export function removeFields<T extends object, K extends keyof T>(
  obj: T | null,
  keys: K[]
): Omit<T, K> | null {
  if(obj){
    const result = { ...obj };
    for (const key of keys) {
      delete result[key];
    }
    return result;
  }
  return null;
}