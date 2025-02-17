import axios from "axios";

const services = {
    auth_service: process.env.REACT_APP_API_URL || 'http://localhost:8001',
    news_service: process.env.REACT_APP_NEWS_SERVICE_URL || 'http://localhost:8005',
};

export const authApi = axios.create({baseURL: services.auth_service});
export const newsApi = axios.create({baseURL: services.news_service});