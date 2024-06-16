import React, { useCallback } from 'react';
import compress from 'compress-base64';

const ImageUploader = () => {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files[0]) {
      const file = files[0];

      if (typeof FileReader === 'function') {
        const reader = new FileReader();
        reader.onload = event => {
          const result = event.target?.result;
          if (result) {
            compress(result, {
              width: 400,
              type: 'image/png',
              max: 200, // max size in KB
              min: 20,  // min size in KB
              quality: 0.8,
            }).then(compressedResult => {
              console.log(compressedResult);
              // Further actions like setting state or uploading to a server
            });
          }
        };
        reader.readAsDataURL(file);
      } else {
        alert('Your browser does not support FileReader');
      }
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
    </div>
  );
};

export default ImageUploader;
