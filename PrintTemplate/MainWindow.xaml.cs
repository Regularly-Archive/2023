using Microsoft.Web.WebView2.Core;
using System;
using System.Drawing.Printing;
using System.IO;
using System.Windows;
using System.Windows.Forms;
using DotLiquid;
using PdfiumViewer;
using System.Drawing;

namespace PrintTemplate
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : System.Windows.Window
    {
        public MainWindow()
        {
            InitializeComponent();
            InitializeViewView2();
        }


        private async void InitializeViewView2()
        {
            await this.webView.EnsureCoreWebView2Async();
        }

        private async void btnHtml_Click(object sender, RoutedEventArgs e)
        {
            // 加载并渲染模板
            var htmlContent = File.ReadAllText("HtmlTemplate.html");
            var template = DotLiquid.Template.Parse(htmlContent);
            htmlContent = template.Render(Hash.FromAnonymousObject(new
            {
                Unit = "XXX公司",
                PickupDate = DateTime.Now.ToString("yyyy-MM-dd hh:mm:ss"),
                OrderNo = "2023092112138",
                TransNo = "2023092112138",
                Location = "西安",
                ProductName = "撒哈拉沙漠里的一滴水",
                CarNo = "陕A12345",
                PlanAmount = 120,
                DriverName = "飞鸿踏雪",
                ActualAmount = 100,
                Remark = "这是通过打印模板渲染的内容",
                QRCode = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQAQAAAACoxAthAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QAAd2KE6QAAAAJcEhZcwAAFxEAABcRAcom8z8AAAIwSURBVHja7dtLbsIwEAbgiViwzBFylByNHM1H4QgsWaBM43nFrkqLTWlZ/CMUodZfV7888aPEzUUgICAg70Yo6sgL0Wn70Y3owOmQR5wHPu8jQEC6yGiBW47ylJFJhwxCBhtwAQHpJZZJIVsmZyGzfCmSCQLyPyQrHSkTJoOA/Dbhq4/UcPpsCQLyJNGyjiytOM97t4ebOAjI9yRKZz9ZU9hnz6QWCEgPqUqmviSxtBo+jQAB6SG6NxIrhSRjZ22vRNP2ozU/LwQC0kXkm/VWtQd5hds+28jVmmwVSxCQRrKvQ7109lPisSzaKwjIn5CtF5+u+fQhkpyfa542p9Wa88ggID1E08a+bi3f+mb2jrwXCEgzySWBtGT6KaqtXimqelEEAWkg+tbnvzh5IFnaq1W2RSxBQJoI22kCe29NflaVqnmv6MggIE3kQkqWuHTEojSWg6wRcj4NgoB0kPzUNULswumLXBy7fzVbgoA8SHRGK9urHSWImnw1Wm53gIC8muQkX22StNIXP7/YpnWuN1VAQB4neuloW7eWh1yWzFi91gcQICBNpCy9PEl+ty2OtwwSCEgPoajiEjjr4sJPUfXdb2QQkC4y7plcyDKZ4u9oLEFAniOaycU3SSyWVO30lrtwICDdJCrRfrGN6v1eEJBnSHmxjSSWk8x7cs3j7v9YgYC8gmgtR46tkuSbw+xnEHSniYOA/Eyi/Cx1DqUbI2tslYCA9JDGAgEBAXkr8gGsyEbTHWX+MAAAAABJRU5ErkJggg=="
            }));

            // 加载网页并截图
            this.webView.Reload();
            this.webView.NavigateToString(htmlContent);
            using (var fileStream = File.OpenWrite("output.jpg"))
            {
                await webView.CoreWebView2.CapturePreviewAsync(CoreWebView2CapturePreviewImageFormat.Jpeg, fileStream);
            };

            // 打印内容
            var printDocument = new PrintDocument();
            printDocument.PrintController = new StandardPrintController();
            printDocument.DefaultPageSettings.PrinterSettings.PrinterName = "HP LaserJet Pro MFP M126nw";
            //foreach (PaperSize paperSize in printDocument.DefaultPageSettings.PrinterSettings.PaperSizes)
            //{
            //    if (paperSize.PaperName == "A5")
            //    {
            //        printDocument.DefaultPageSettings.PaperSize = paperSize;
            //    }
            //}
            printDocument.DefaultPageSettings.Landscape = true;
            printDocument.PrintPage += async (s, e) =>
            {
                e.Graphics.InterpolationMode = System.Drawing.Drawing2D.InterpolationMode.NearestNeighbor;
                e.Graphics.PixelOffsetMode = System.Drawing.Drawing2D.PixelOffsetMode.Half;

                var m = printDocument.DefaultPageSettings.PrintableArea;
                var image = System.Drawing.Image.FromFile("output.jpg");
                var scale = image.Width / image.Height;
                e.Graphics.DrawImage(image, new System.Drawing.RectangleF(m.Left, m.Top, m.Width, m.Width / scale));
            };
            var printPreviewDialog = new PrintPreviewDialog { Document = printDocument };
            printPreviewDialog.TopLevel = true;
            printPreviewDialog.Document = printDocument;
            printPreviewDialog.ShowDialog();
        }


        private async void btnSvg_Click(object sender, RoutedEventArgs e)
        {
            // 加载并渲染模板
            var svgContent = File.ReadAllText("pattern.svg");

            // 加载网页并截图
            this.webView.Reload();
            this.webView.NavigateToString(svgContent);
            using (var fileStream = File.OpenWrite("output.jpg"))
            {
                await webView.CoreWebView2.PrintToPdfAsync("output.pdf");
                await webView.CoreWebView2.CapturePreviewAsync(CoreWebView2CapturePreviewImageFormat.Jpeg, fileStream);
            };

            // 打印内容
            var printDocument = new PrintDocument();
            printDocument.PrintController = new StandardPrintController();
            printDocument.DefaultPageSettings.PrinterSettings.PrinterName = "HP LaserJet Pro MFP M126nw";
            printDocument.DefaultPageSettings.Landscape = true;
            printDocument.PrintPage += async (s, e) =>
            {
                //var m = printDocument.DefaultPageSettings.PrintableArea;
                //var image = System.Drawing.Image.FromFile("output.jpg");
                //var scale = image.Width / image.Height;
                //e.Graphics.DrawImage(image, new System.Drawing.RectangleF(m.Left, m.Top, m.Width, m.Width / scale));

                //using (PdfDocument pdfDocument = PdfDocument.Load("output.pdf"))
                //{
                //    using (Bitmap bitmap = new Bitmap(pdfDocument.PageSizes[0].Width, pdfDocument.PageSizes[0].Height))
                //    {
                //        pdfDocument.Render(e.PageIndex, bitmap);
                //        args.Graphics.DrawImage(bitmap, args.MarginBounds);
                //    }
                //}
            };
            var printPreviewDialog = new PrintPreviewDialog { Document = printDocument };
            printPreviewDialog.Document = printDocument;
            printPreviewDialog.ShowDialog();
        }

        private void btnXaml_Click(object sender, RoutedEventArgs e)
        {
            var filePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "原型.pdf");
            using (PdfDocument document = PdfDocument.Load(filePath))
            {
                using (PrintDocument printDoc = new PrintDocument())
                {
                    printDoc.PrinterSettings.PrintFileName = filePath;
                    printDoc.PrinterSettings.PrintToFile = false;
                    printDoc.PrinterSettings.FromPage = 1;
                    printDoc.PrinterSettings.ToPage = document.PageCount;
                    printDoc.PrinterSettings.PrintRange = PrintRange.AllPages;
                    printDoc.PrinterSettings.DefaultPageSettings.Landscape = document.PageSizes[0].Width > document.PageSizes[0].Height;
                    printDoc.DefaultPageSettings.Margins = new Margins(0, 0, 0, 0);

                    printDoc.PrintPage += (sender, e) =>
                    {
                        using (Image image = document.Render(e.PageSettings.PrinterSettings.FromPage, 96, 96, true))
                        {
                            e.Graphics.DrawImage(image, e.PageBounds);
                            e.HasMorePages = e.PageSettings.PrinterSettings.FromPage < e.PageSettings.PrinterSettings.ToPage;
                            e.PageSettings.PrinterSettings.FromPage++;
                        }
                    };

                    // printDoc.Print();

                    var printPreviewDialog = new PrintPreviewDialog { Document = printDoc };
                    printPreviewDialog.TopLevel = true;
                    printPreviewDialog.Document = printDoc;
                    printPreviewDialog.ShowDialog();
                }
            }
        }
    }
}
