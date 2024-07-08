// src/services/changelogService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/changelog/';

const getChangelogs = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error('Error fetching changelogs:', error);
        throw error;
    }
};

export default {
    getChangelogs,
};
