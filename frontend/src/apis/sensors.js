import { BASE_URL } from "../lib/config";

export const getAllSensors = async () => {
  const response = await fetch(`${BASE_URL}/sensors`);
  return response.json();
};