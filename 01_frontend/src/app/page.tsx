"use client"

import React, { useState } from 'react';

const HomePage = () => {
  const [ url, setUrl ] = useState('');
  const [ preference, setPreference ] = useState(1);
  const [ outputPath, setOutputPath ] = useState('downloads');
  const [ message, setMessage ] = useState('');
  const [ error, setError ] = useState('');

  const downloadVideo = async () => {
    try {

      const response = await fetch(
        '/api/youtube_downloader', 
        {
          method: 'POST',
          headers: { 'Content-Type' : 'application/json' },
          body : JSON.stringify({ url, preference, output_path : outputPath })
        }
      )
      const data = await response.json();
      console.log('data : page.tsx : ', data)
      if (response.ok){
        setMessage(data.message);
        setError('');
      } else {
        setMessage('');
        setError(data.error);
      }
    } 
    catch (error) {
      console.log('error : ', error)
      setMessage('');
      setError('Network error');
    }
  }

  return (
    <div>
      {/* Header  */}
      <h1>YouTube Downloader</h1>
      {/* URL Input  */}
      <input 
        type="text"
        placeholder='Enter YouTube URL'
        value={url}
        onChange={(e) => setUrl(e.target.value)} 
      />
      {/* Preference Select  */}
      <select
        value={preference}
        onChange={(e) => setPreference(Number(e.target.value))}
      >
        <option value={1}> Video </option>
        <option value={2}> Audio </option>
      </select>
      {/* Output Path Input  */}
      <input 
        type='text'
        placeholder='Enter file path to save (or) Leave blank for default'
        value={outputPath}
        onChange={(e) => setOutputPath(e.target.value)}
      />
      {/* Download btn  */}
      <button onClick={downloadVideo}> Download </button>

      {
        message && 
        <p style={{color : 'green'}}> {message} </p>
      }
      {
        error && 
        <p style={{ color: 'red'}}>
          {error}
        </p>
      }

    </div>

  )
}

export default HomePage;