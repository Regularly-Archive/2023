using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace USBPOC
{
    public class DeviceNotifierEventArgs
    {
        public string DeviceId { get; set; }
        public string DevicePath { get; set; }
        public string Pid { get; set; }
        public string Vid { get; set; }
    }
}
