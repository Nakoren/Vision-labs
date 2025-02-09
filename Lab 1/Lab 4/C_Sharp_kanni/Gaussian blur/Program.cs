using OpenCvSharp;
using System.Diagnostics;

namespace program
{
    class Program
    {
        static void Main(string[] args)
        {
            Kanni kanMan = new Kanni();
            kanMan.Start();
        }

    }
    
    public class Kanni()
    {
        public void Start()
        {
            string imagePath = @"C:\Users\minen\Desktop\City_shakal.png";

            Mat img = new Mat(imagePath, ImreadModes.Grayscale);
            int coreSize = 3;
            double sigma = 0.5;

            Size kSize = new OpenCvSharp.Size(coreSize, coreSize);
            //using (new OpenCvSharp.Window("Original", img));
            //Mat imgBlur = new Mat();

            Mat imgBlur = new Mat(img.Rows, img.Cols, MatType.CV_8UC4);

            Cv2.GaussianBlur(img, imgBlur, kSize, sigma);

            List<List<double>>[] grads = getGradients(imgBlur);

            List<List<double>> lengths = grads[0];
            List<List<double>> directions = grads[1];

            Mat suppressed = suppressMaximum(imgBlur, directions, lengths); 

            double maxLen = getMaxValueFromMatrix(grads[0]);

            double highLevel = maxLen / 5;
            double lowLevel = maxLen / 10;

            Mat filtered = doubleEdgeFiltration(suppressed, grads[0], lowLevel, highLevel);

            using (new OpenCvSharp.Window("Kanni", filtered, WindowFlags.KeepRatio))
            {
                Size windowSize = new Size(1000, 500);
                Cv2.ResizeWindow("Kanni", windowSize);
                Cv2.WaitKey();
            }
        }

        List<List<double>>[] getGradients(Mat img)
        {

            List<List<double>> lengthMatrix = new List<List<double>>();
            List<List<double>> angleMatrix = new List<List<double>>();
            
            for (int i = 0; i < img.Rows; i++)
            {
                lengthMatrix.Add(new List<double>());
                angleMatrix.Add(new List<double>());
                for (int j = 0; j < img.Cols; j++) {
                    lengthMatrix[i].Add(0);
                    angleMatrix[i].Add(-1);
                }
            }

            int[][] xKernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];
            int[][] yKernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]];

            var test = img.Get<byte>();

            for (int i = 1; i < img.Height - 1; i++)
            {
                for (int j = 1; j < img.Width - 1; j++)
                {
                    float xLocalRes = 0;
                    float yLocalRes = 0;
                    for (int k = -1; k <=1 ; k++)
                    {
                        for (int n = -1; n <= 1; n++)
                        {
                            xLocalRes += img.At<byte>(i + k, j + n) * xKernel[k+1][n+1];
                            yLocalRes += img.At<byte>(i + k, j + n) * yKernel[k+1][n+1];
                        }
                    }
                    if (xLocalRes == 0)
                    {
                        xLocalRes = (float)0.0001;
                    }
                    float len = (float)Math.Sqrt(Math.Pow(xLocalRes, 2) + Math.Pow(yLocalRes, 2));
                    lengthMatrix[i][j]=len;

                    double tangRes = Math.Tan((float)(yLocalRes / xLocalRes));
                    int finRes = -1;
                    if ((xLocalRes > 0 && yLocalRes < 0 && tangRes < -2.414) || (xLocalRes < 0 && yLocalRes < 0 && tangRes > 2.414)) 
                        finRes = 0;
                    else if (xLocalRes > 0 && yLocalRes < 0 && tangRes < -0.414)
                        finRes = 1;
                    else if ((xLocalRes > 0 && yLocalRes < 0 && tangRes > -0.414) || (xLocalRes > 0 && yLocalRes > 0 && tangRes < 0.414))
                        finRes = 2;
                    else if (xLocalRes > 0 && yLocalRes > 0 && tangRes < 2.414)
                        finRes = 3;
                    else if ((xLocalRes > 0 && yLocalRes > 0 && tangRes > 2.414) || (xLocalRes < 0 && yLocalRes > 0 && tangRes > -2.414))
                        finRes = 4;
                    else if (xLocalRes < 0 && yLocalRes > 0 && tangRes < -0.414)
                        finRes = 5;
                    else if ((xLocalRes < 0 && yLocalRes > 0 && tangRes > -0.414) || (xLocalRes < 0 && yLocalRes < 0 && tangRes < 0.414))
                        finRes = 6;
                    else if (xLocalRes < 0 && yLocalRes < 0 && tangRes < 2.414)
                        finRes = 7;
                    angleMatrix[i][j] = finRes;
                    //Console.WriteLine(angleMatrix[i][j]);
                }
            }
            //CheckMat(angleMatrix);
            return [lengthMatrix, angleMatrix];
        }

        Mat suppressMaximum(Mat img, List<List<double>> directions, List<List<double>> lengths)
        {
            Mat finMatrix = new Mat<Byte>(img.Rows, img.Cols);
            for (int i = 1; i < img.Rows - 1; i++)
            {
                for (int j = 1; j < img.Width - 1; j++)
                {
                    bool check = false;
                    if ((directions[i][j] == 0) || (directions[i][j] == 4))
                    {
                        if ((lengths[i][j] > lengths[i][j] && (lengths[i][j] > lengths[i-1][j])))
                        {
                            check = true;
                        }
                    }
                    else if ((directions[i][j] == 1) && (directions[i][j] == 5))
                    {
                        if ((lengths[i][j] > lengths[i+1][j+1]) && (lengths[i][j] > lengths[i-1][j-1]))
                        {
                            check = true;
                        }
                    }
                    else if ((directions[i][j] == 2) || (directions[i][j] == 6))
                    {
                        if ((lengths[i][j] > lengths[i][j+1]) && (lengths[i][j] > lengths[i][j-1]))
                        {
                            check = true;
                        }
                    }
                    else if ((directions[i][j] == 3) || (directions[i][j] == 7))
                    {
                        if ((lengths[i][j] > lengths[i+1][j-1] && (lengths[i][j] > lengths[i-1][j+1])))
                        {
                            check = true;
                        }
                    }
                    if (check)
                    {
                        finMatrix.Set(i, j, (Byte)255);
                    }
                    else
                    {
                        finMatrix.Set(i, j, (Byte)0);
                    }
                }
            }
            return finMatrix;
        }
        double getMaxValueFromMatrix(List<List<double>> matr)
        {
            double max = 0;
            for (int i = 0; i < matr.Count; i++)
            {
                for (int j = 0; j < matr[i].Count; j++)
                {
                    double cur = matr[i][j];
                    if (cur > max)
                    {
                        max = cur;
                    }
                }
            }
            return max;
        }

        Mat doubleEdgeFiltration(Mat img, List<List<double>> matLen, double lowLevel, double highLevel)
        {
            Mat finMat = new Mat<Byte>(img.Rows, img.Cols);
            for (int i = 0; i < img.Rows; i++)
            {
                for (int j = 0; j < img.Width; j++)
                {
                    if (img.Get<byte>(i, j) == 255)
                    {
                        double curLen = matLen[i][j];
                        if (curLen > highLevel)
                        {
                            finMat.Set(i, j, (Byte)255);
                        }
                        else
                        {
                            finMat.Set(i, j, (Byte)0);
                        }
                    }
                }
            }
            for (int i = 1; i < img.Rows - 1; i++)
            {
                for (int j = 1; j < img.Width - 1; j++)
                {
                    double curLen = matLen[i][j];
                    if ((curLen > lowLevel) && (curLen < highLevel))
                    {
                        bool check = false;
                        for (int k = -1; k <= 1; k++)
                        {
                            for (int n = -1; n <= 1; n++)
                            {
                                if (finMat.Get<byte>(i + k, j + n) == 255)
                                {
                                    check = true; break;
                                }
                            }
                        }
                        if (check)
                        {
                            finMat.Set(i, j, (Byte)255);
                        }
                    }
                }
            }
            return finMat;
        }
        void CheckMat(List<List<double>> mat)
        {
            for (int i = 0;i < mat.Count;i++)
            {
                for(int j = 0;j < mat[i].Count; j++)
                {
                    double test = mat[i][j];
                    Console.Write(test);
                }
            }
            Console.WriteLine('\n');
        }
    }
}