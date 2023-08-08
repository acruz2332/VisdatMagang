const mongoose = require('mongoose');

const processed_data = mongoose.model(
            "processed_data", 
            new mongoose.Schema({
                id: String,
                title: String,
                content: String,
                label: String,
                created_date: String,
                created_time: String,
                published_date: String,
                published_time: String,
                keywords: String,
                sumber: String,
                sentimen: String,
            }
        )
    );

module.exports = processed_data;

