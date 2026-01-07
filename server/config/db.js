const mongoose = require('mongoose');
//database connection
const connectDB = async () => {
mongoose.connect("mongodb://127.0.0.1:27017/Minorproject").then(()=>
console.log('database connected sucessfully')).catch((error)=>
console.log('database connection error'))
}

module.exports = connectDB;
