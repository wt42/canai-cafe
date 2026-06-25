const BASE_DATA_PATH = `${import.meta.env.BASE_URL}data/`;

export async function getJson(fileName) {
  const response = await fetch(`${BASE_DATA_PATH}${fileName}`);

  if (!response.ok) {
    throw new Error(`Unable to load ${fileName}. HTTP ${response.status}`);
  }

  return response.json();
}

export async function getManyJson(fileNames) {
  const results = await Promise.all(fileNames.map((fileName) => getJson(fileName)));

  return fileNames.reduce((acc, fileName, index) => {
    acc[fileName] = results[index];
    return acc;
  }, {});
}
