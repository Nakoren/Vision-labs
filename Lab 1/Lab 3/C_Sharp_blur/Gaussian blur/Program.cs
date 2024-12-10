using OpenCvSharp;
using System.Diagnostics;

namespace program
{
    class Program
    {
        static void Main(string[] args)
        {
            string imagePath = @"C:\Users\minen\Desktop\Unik\Vision\Pic_compressed.jpg";

            Mat img = new Mat(imagePath, ImreadModes.Grayscale);
            int coreSize = 5;
            double sigma = 3;

            Size cvSize = new Size(coreSize, coreSize);
            //using (new OpenCvSharp.Window("Original", img));
            //Mat imgBlur = new Mat();
            double[][] Gaussiankernel = GetGaussianMatrix(coreSize, sigma);
            Mat imgBlur = gaussianBlur(img, img.Size().Height, img.Size().Width, Gaussiankernel, coreSize);
  
            
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

        static double[][] GetGaussianMatrix(int size, double deviation)
        {
            double mExp = Math.Ceiling((double)(size / 2))+1    ;
            double[][] resMatrix = new double[size][];
            for(int i = 0; i < size; i++)
            {
                resMatrix[i] = new double[size];
            }
            for(int x = 0; x < size; x++)
            {
                for(int y = 0; y < size; y++)
                {

                    double sqrDev = Math.Pow(deviation, 2);
                    double power = -1 * (((Math.Pow((x - mExp), 2) + (Math.Pow((x - mExp), 2))))) / sqrDev;

                    resMatrix[y][x] = 1/(2*Math.PI * sqrDev) * Math.Exp(power);
                }
            }

            double sum = 0;
            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    sum += resMatrix[y][x];
                }
            }

            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    resMatrix[y][x] = resMatrix[y][x] / sum;
                }
            }


            return resMatrix;
        }
        static Mat gaussianBlur(Mat source, int sourceHeight, int sourceLength, double[][] kernel, int kernelSize)
        {
            Mat res = new Mat();
            source.CopyTo(res);

            int coreCenter = (int)Math.Ceiling((double)(kernelSize / 2));

            for(int sLen = coreCenter; sLen< sourceLength - coreCenter; sLen++)
            {
                for(int sHei = coreCenter; sHei< sourceHeight - coreCenter; sHei++)
                {
                    double newValue = 0;
                    for (int matrLen= -coreCenter; matrLen<= coreCenter; matrLen++) {
                        for(int  matrHei= -coreCenter; matrHei<= coreCenter; matrHei++)
                        {
                            //Console.WriteLine(i + " " + j + " " + k + " " + l + " " + newValue);
                            
                            byte prevValue = source.At<byte>(sHei + matrHei, sLen + matrLen);
                            double modif = kernel[matrLen + coreCenter][matrHei + coreCenter];
                            newValue += (prevValue * modif);
                        }
                    }
                    //Console.WriteLine(i + " " + j + " " + newValue);
                    res.Set<byte>(sHei,sLen, (byte)newValue);
                }
                
            }
            return res;
        }
    }
}