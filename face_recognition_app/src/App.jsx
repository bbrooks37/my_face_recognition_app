import { useState } from 'react';
import { CameraIcon, UploadCloudIcon, RefreshCcwIcon } from 'lucide-react';

// Main App component
const App = () => {
  // State for the two image files
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  
  // State for the preview URLs
  const [preview1, setPreview1] = useState(null);
  const [preview2, setPreview2] = useState(null);
  
  // State for the similarity score and loading status
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle file selection for the first image
  const handleImage1 = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage1(file);
      setPreview1(URL.createObjectURL(file));
      setScore(null); // Reset score when a new image is uploaded
    }
  };

  // Handle file selection for the second image
  const handleImage2 = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage2(file);
      setPreview2(URL.createObjectURL(file));
      setScore(null); // Reset score when a new image is uploaded
    }
  };

  // Simulate a comparison API call
  const handleCompare = async () => {
    if (!image1 || !image2) {
      alert("Please upload two images to compare.");
      return;
    }

    setLoading(true);
    setScore(null);

    // Simulate an API call with a 2-second delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Simulate a hardcoded similarity score
    const simulatedScore = Math.random() * 0.3 + 0.5; // Generate a score between 0.5 and 0.8
    setScore(simulatedScore);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 flex flex-col items-center justify-center p-4 font-sans">
      <div className="bg-gray-800 shadow-2xl rounded-3xl p-8 max-w-4xl w-full mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-5xl font-extrabold tracking-tight text-white mb-2">
            Family Face Similarity
          </h1>
          <p className="text-lg text-gray-400">
            Upload two photos to compare their facial similarity.
          </p>
        </div>

        {/* Upload and Display Section */}
        <div className="flex flex-col md:flex-row justify-center items-center gap-8 mb-8">
          {/* Image Upload 1 */}
          <div className="flex flex-col items-center w-full md:w-1/2">
            <label 
              htmlFor="upload1" 
              className="w-full h-64 border-4 border-dashed border-gray-600 rounded-2xl flex flex-col items-center justify-center cursor-pointer transition-all duration-300 hover:border-blue-500 hover:bg-gray-700"
            >
              {preview1 ? (
                <img src={preview1} alt="Uploaded Image 1" className="h-full w-full object-contain rounded-xl p-2"/>
              ) : (
                <>
                  <UploadCloudIcon size={48} className="text-gray-500 mb-2"/>
                  <span className="text-gray-500">Upload First Image</span>
                </>
              )}
            </label>
            <input 
              id="upload1" 
              type="file" 
              accept="image/*" 
              onChange={handleImage1} 
              className="hidden"
            />
          </div>

          {/* Image Upload 2 */}
          <div className="flex flex-col items-center w-full md:w-1/2">
            <label 
              htmlFor="upload2" 
              className="w-full h-64 border-4 border-dashed border-gray-600 rounded-2xl flex flex-col items-center justify-center cursor-pointer transition-all duration-300 hover:border-blue-500 hover:bg-gray-700"
            >
              {preview2 ? (
                <img src={preview2} alt="Uploaded Image 2" className="h-full w-full object-contain rounded-xl p-2"/>
              ) : (
                <>
                  <UploadCloudIcon size={48} className="text-gray-500 mb-2"/>
                  <span className="text-gray-500">Upload Second Image</span>
                </>
              )}
            </label>
            <input 
              id="upload2" 
              type="file" 
              accept="image/*" 
              onChange={handleImage2} 
              className="hidden"
            />
          </div>
        </div>

        {/* Compare Button */}
        <div className="flex justify-center mb-8">
          <button
            onClick={handleCompare}
            disabled={!image1 || !image2 || loading}
            className={`px-8 py-4 text-xl font-bold rounded-full transition-all duration-300 shadow-lg
              ${(image1 && image2) && !loading
                ? 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-xl'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
              }`
            }
          >
            {loading ? (
              <RefreshCcwIcon className="animate-spin" size={24}/>
            ) : (
              'Compare Faces'
            )}
          </button>
        </div>

        {/* Results Section */}
        {score && (
          <div className="bg-gray-700 rounded-2xl p-6 text-center shadow-lg transition-opacity duration-500 opacity-100">
            <h3 className="text-3xl font-extrabold text-white mb-2">
              Similarity Score
            </h3>
            <p className="text-5xl font-extrabold text-blue-400 mb-2">
              {score.toFixed(4)}
            </p>
            <p className="text-gray-400">
              A lower score indicates a closer resemblance.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
