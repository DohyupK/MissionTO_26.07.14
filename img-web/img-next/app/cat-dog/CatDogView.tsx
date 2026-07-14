'use client'
import { useState } from "react";
import axios from "axios";

export default function CatDogView() {

    const [file, setFile] = useState<File | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            console.log(file);
            setFile(file);
        }
    }

    const handleUpload = async () => {
        console.log('Upload');
        if (file) {
            const formData = new FormData();
            formData.append('image', file);
            const response = await axios.post('http://127.0.0.1:5000/predict', formData)
            console.log(response.data);
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 flex items-center justify-center p-6 font-sans">
            <div className="bg-white/70 backdrop-blur-xl rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-white/50 p-8 max-w-md w-full flex flex-col items-center gap-8 transition-all duration-300 hover:shadow-[0_8px_40px_rgb(0,0,0,0.16)]">
                <div className="text-center space-y-2">
                    <h1 className="text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 tracking-tight">
                        CatDogView
                    </h1>
                    <p className="text-gray-500 text-sm font-medium">Upload an image to classify</p>
                </div>
                
                <div className="w-full group">
                    <label className="relative flex flex-col items-center justify-center w-full h-48 border-2 border-indigo-200 border-dashed rounded-2xl cursor-pointer bg-white/50 hover:bg-indigo-50/50 hover:border-indigo-400 transition-all duration-300 overflow-hidden">
                        <div className="flex flex-col items-center justify-center pt-5 pb-6 px-4 text-center z-10">
                            <div className="p-3 bg-indigo-100 rounded-full mb-4 group-hover:scale-110 transition-transform duration-300 group-hover:bg-indigo-200">
                                <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                                </svg>
                            </div>
                            <p className="mb-1 text-sm font-semibold text-gray-700">
                                {file ? file.name : "Click to select or drag and drop"}
                            </p>
                            <p className="text-xs text-gray-500">
                                {file ? "Ready to upload" : "SVG, PNG, JPG or GIF"}
                            </p>
                        </div>
                        {/* Background subtle gradient */}
                        <div className="absolute inset-0 bg-gradient-to-t from-indigo-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <input type="file" className="hidden" onChange={handleFileChange} accept="image/*" />
                    </label>
                </div>

                <button 
                    onClick={handleUpload}
                    disabled={!file}
                    className={`relative w-full py-4 px-6 rounded-2xl font-bold text-lg overflow-hidden transition-all duration-300 transform
                        ${file 
                            ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg hover:shadow-indigo-500/30 hover:-translate-y-1 hover:scale-[1.02] active:scale-95" 
                            : "bg-gray-200 text-gray-400 cursor-not-allowed"}`}
                >
                    <span className="relative z-10 flex items-center justify-center gap-2">
                        Upload
                        {file && (
                            <svg className="w-5 h-5 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                            </svg>
                        )}
                    </span>
                </button>
            </div>
        </div>
    )
}