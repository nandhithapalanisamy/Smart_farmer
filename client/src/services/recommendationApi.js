import axios from "axios";

const API = axios.create({
  baseURL: "",
});

export const getCropRecommendation = async (formData) => {
  try {
    const response = await API.post(
      "/api/recommend",
      formData
    );

    return response.data;

  } catch (error) {

    throw new Error(
      error.response?.data?.message ||
      "Failed to get recommendation."
    );

  }
};

export const getCropDetails = async (cropName) => {

  try {

    const response = await API.get(
      `/api/crop/${cropName}`
    );

    return response.data;

  } catch (error) {

    throw new Error(
      error.response?.data?.message ||
      "Unable to fetch crop details."
    );

  }

};

