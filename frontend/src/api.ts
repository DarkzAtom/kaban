import axios from "axios";

const services = {
    auth_service: process.env.REACT_APP_API_URL || 'http://localhost:8000',
};

export const authApi = axios.create({baseURL: services.auth_service});