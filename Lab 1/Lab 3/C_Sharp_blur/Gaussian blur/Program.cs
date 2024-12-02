using OpenCvSharp;

namespace program
{
    class Program
    {
        static void Main(string[] args)
        {
            string imagePath = @"C:\Users\minen\Desktop\Unik\Vision\Pic_compressed.jpg";

            Mat img = new Mat(imagePath, ImreadModes.Grayscale);
            int coreSize = 11;
            double sigma = 0;

            Size cvSize = new Size(coreSize, coreSize);
            //using (new OpenCvSharp.Window("Original", img));
            Mat imgBlur = new Mat();
            Cv2.GaussianBlur(img, imgBlur, cvSize, sigma);
            
            using (new OpenCvSharp.Window("Normal", img, WindowFlags.KeepRatio))
            {
                Size windowSize = new Size(1000, 500);
                Cv2.ResizeWindow("Normal", windowSize);
                Cv2.WaitKey();
            }

            using (new OpenCvSharp.Window("Blur", imgBlur, WindowFlags.KeepRatio))
            {
                Size windowSize = new Size(1000,500);
                Cv2.ResizeWindow("Blur",windowSize);
                Cv2.WaitKey();
            }
        }
    }
}