export function randomKeyFromObject(object) {
  const keys = Object.keys(object);
  const index = Math.floor(Math.random() * keys.length)
  return keys[index]
}
