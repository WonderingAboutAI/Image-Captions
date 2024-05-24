# Image-Captions
This Python script uses OpenAI's GPT-4-Turbo model to generate image captions and then store them alongside the corresponding image file names into a .csv file. It's useful if you need to generate numerous captions for updating alt tags on your website, training machine learning models, etc. 

## About the script

### Environment Setup
The script begins by loading necessary environment variables using the dotenv library. This includes retrieving the API key for OpenAI from a local .env file, which is needed to authenticate API requests.

### Directory Setup
It defines a directory containing images and a path for the output CSV file where captions will be stored.

### Image Handling
The script includes a function, resize_and_encode_image, that opens each image, resizes it to a specified dimension (256x256 pixels by default), compresses it, and encodes it in base64 format. This function handles errors by logging any issues encountered during processing.

### Base64 Encoding
After resizing and compression, images are converted into a base64 string format, suitable for web transmission or API usage.

### Caption Generation
It uses the OpenAI API to generate captions for each processed image using the GPT-4-Turbo model with Computer Vision. The API is called with a base64 encoded image, and the script expects to receive text describing  the image content. Any issues in caption generation due to API errors are logged.

```
Always store API keys and sensitive information in environment variables or secure configuration files like .env to minimize the risk of exposure and to comply with best security practices.
```

### Data Storage
Captions along with the filenames are stored in a list of dictionaries.

### Output to CSV
Finally, the data is compiled into a pandas DataFrame and exported to a CSV file, making it easy to review and utilize the generated captions.

## A word about rate limits
if you're planning to create captions for a very large number of images with a new OpenAI account, you may exceed rate limits for the API. Rate limits exist to manage the load on the infrastructure powering AI models. If you exceed them, you'll get an error message like "Too many requests" or "Rate limit error."

See OpenAI's documentation for more information on rate limits and how you can manage processing in your scripts to avoid exceeding them: 

## Summary
This script can save you time if you need to caption nnumerous images for whatever reason. You can adjust the prompt to specify a word count and tone of voice that's most appropriate for your project.
