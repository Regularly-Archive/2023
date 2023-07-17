using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.StaticFiles;
using Microsoft.Extensions.FileProviders;
using System.IO;
using Microsoft.AspNetCore.Hosting;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace VideoService.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FilesController : ControllerBase
    {
        private readonly IHostEnvironment _hostEnvironment;
        public FilesController(IHostEnvironment hostEnvironment)
        {
            _hostEnvironment = hostEnvironment;
        }

        [HttpGet("download")]
        public ActionResult Download([FromQuery] string fileName)
        {
            var filePath = Path.Combine(_hostEnvironment.ContentRootPath, "Assets", fileName);
            if (!System.IO.File.Exists(filePath)) return NotFound();

            var contentType = GetContentType(filePath);
            var fileStream = System.IO.File.OpenRead(filePath);

            return File(fileStream, contentType, enableRangeProcessing: true);
        }

        private string GetContentType(string filePath)
        {
            string suffix = Path.GetExtension(filePath);
            var provider = new FileExtensionContentTypeProvider();
            return provider.Mappings[suffix];
        }
    }
}
