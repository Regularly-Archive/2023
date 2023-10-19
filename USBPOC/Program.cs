using LibUsbDotNet;
using LibUsbDotNet.Main;
using LibUsbDotNet.Info;
using System.Collections.ObjectModel;
using System.Management;
using Microsoft.Extensions.Logging;
using LibUsbDotNet.DeviceNotify;
using LibUsbDotNet.Main;
using LibUsbDotNet.WinUsb;
using LibUsbDotNet.DeviceNotify.Info;
using System.Text.Json.Serialization;
using Newtonsoft.Json;
using System.Security.Cryptography;
using System.Text.RegularExpressions;
using System.Text;
using LibUsbDotNet.DeviceNotify;
using LibUsbDotNet.DeviceNotify.Linux;
using LibUsbDotNet.LibUsb;

namespace USBPOC
{
    public class Program
    {
        public static void PrintUsbInfo()
        {
            UsbDevice usbDevice = null;
            UsbRegDeviceList allDevices = UsbDevice.AllDevices;

            Console.WriteLine("Found {0} devices", allDevices.Count);

            foreach (UsbRegistry usbRegistry in allDevices)
            {
                Console.WriteLine("Got device: {0}\r\n", usbRegistry.FullName);

                if (usbRegistry.Open(out usbDevice))
                {
                    Console.WriteLine("Device Information\r\n------------------");

                    Console.WriteLine("{0}", usbDevice.Info.ToString());

                    Console.WriteLine("VID & PID: {0} {1}", usbDevice.Info.Descriptor.VendorID, usbDevice.Info.Descriptor.ProductID);

                    Console.WriteLine("\r\nDevice configuration\r\n--------------------");
                    foreach (UsbConfigInfo usbConfigInfo in usbDevice.Configs)
                    {
                        Console.WriteLine("{0}", usbConfigInfo.ToString());

                        Console.WriteLine("\r\nDevice interface list\r\n---------------------");
                        ReadOnlyCollection<UsbInterfaceInfo> interfaceList = usbConfigInfo.InterfaceInfoList;
                        foreach (UsbInterfaceInfo usbInterfaceInfo in interfaceList)
                        {
                            Console.WriteLine("{0}", usbInterfaceInfo.ToString());

                            Console.WriteLine("\r\nDevice endpoint list\r\n--------------------");
                            ReadOnlyCollection<UsbEndpointInfo> endpointList = usbInterfaceInfo.EndpointInfoList;
                            foreach (UsbEndpointInfo usbEndpointInfo in endpointList)
                            {
                                Console.WriteLine("{0}", usbEndpointInfo.ToString());
                            }
                        }
                    }
                    usbDevice.Close();
                }
                Console.WriteLine("\r\n----- Device information finished -----\r\n");
            }
        }

        private static bool HasUsbDevice(short vid, short pid)
        {
            var useDeviceFinder = new UsbDeviceFinder(vid, pid);
            var usbDevice = UsbDevice.OpenUsbDevice(useDeviceFinder);
            return usbDevice != null;
        }

        private static bool HasUsbDevice2(string vid, string pid)
        {
            var query = $"SELECT * FROM Win32_PnPEntity WHERE DeviceID LIKE 'USB%VID_{vid}&PID_{pid}%'";
            var searcher = new ManagementObjectSearcher(query);
            var devices = searcher.Get();
            return devices.Count > 0;
        }

        private static void MonitorUsbDevice()
        {
            // 监听 USB 设备插入
            var queryInsert = new WqlEventQuery("SELECT * FROM __InstanceCreationEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_USBControllerDevice'");
            var watcherInsert = new ManagementEventWatcher(queryInsert);
            watcherInsert.EventArrived += (sender, e) =>
            {
                // 被插入的逻辑处理
                var targetInstance = (ManagementBaseObject)e.NewEvent["TargetInstance"];
                // \\SNOWFLY-PC\root\cimv2:Win32_PnPEntity.DeviceID="HID\\VID_0000&PID_3825\\6&2BE8ADFA&0&0000"
                var deviceId = targetInstance.Properties["Dependent"].Value.ToString();
                var device = new ManagementObject(deviceId);

                var args = new DeviceNotifierEventArgs();
                // Win32_PnPEntity.DeviceID="HID\\VID_0000&PID_3825\\6&2BE8ADFA&0&0000"
                args.DeviceId = device.Path.RelativePath.Split("=")[1].Replace("\"", "");
                args.DevicePath = device.Path.ToString();
                args.Pid = "0x" + deviceId.Split(new char[] { '&', '\\' }).FirstOrDefault(x => x.StartsWith("PID_")).Replace("PID_", "");
                args.Vid = "0x" + deviceId.Split(new char[] { '&', '\\' }).FirstOrDefault(x => x.StartsWith("VID_")).Replace("VID_", "");
                if (!args.DeviceId.StartsWith("USB")) return;
                Console.WriteLine($"设备已插入 => {JsonConvert.SerializeObject(args)}");
            };
            watcherInsert.Start();

            var queryDelete = new WqlEventQuery("SELECT * FROM __InstanceDeletionEvent WITHIN 1 WHERE TargetInstance ISA 'Win32_USBControllerDevice'");
            var watcherDelete = new ManagementEventWatcher(queryDelete);
            watcherDelete.EventArrived += (sender, e) =>
            {
                // 被拔出的逻辑处理
                var targetInstance = (ManagementBaseObject)e.NewEvent["TargetInstance"];
                // \\SNOWFLY-PC\root\cimv2:Win32_PnPEntity.DeviceID="HID\\VID_0000&PID_3825\\6&2BE8ADFA&0&0000"
                var deviceId = targetInstance.Properties["Dependent"].Value.ToString();
                var device = new ManagementObject(deviceId);

                var args = new DeviceNotifierEventArgs();
                // Win32_PnPEntity.DeviceID="HID\\VID_0000&PID_3825\\6&2BE8ADFA&0&0000"
                args.DeviceId = device.Path.RelativePath.Split("=")[1].Replace("\"", "");
                args.DevicePath = device.Path.ToString();
                args.Pid = "0x" + deviceId.Split(new char[] { '&', '\\' }).FirstOrDefault(x => x.StartsWith("PID_")).Replace("PID_", "");
                args.Vid = "0x" + deviceId.Split(new char[] { '&', '\\' }).FirstOrDefault(x => x.StartsWith("VID_")).Replace("VID_", "");
                if (!args.DeviceId.StartsWith("USB")) return;
                Console.WriteLine($"设备已拔出 => {JsonConvert.SerializeObject(args)}");
            };
            watcherDelete.Start();
        }

        public static void Main(string[] args)
        {
            // 通过 LibUsbDotNet 判断 USB 设备是否存在
            var verdorId = Convert.ToInt16("0x0000", 16);
            var productId = Convert.ToInt16("0x3825", 16);
            if (HasUsbDevice(verdorId, productId))
            {
                Console.WriteLine("[LibUsbDotNet]设备已连接");
            }
            else
            {
                Console.WriteLine("[LibUsbDotNet]设备未连接");
            }

            // 通过 WMI 判断 USB 设备是否存在
            if (HasUsbDevice2("0000", "3825"))
            {
                Console.WriteLine("[WMI]设备已连接");
            }
            else
            {
                Console.WriteLine("[WMI]设备未连接");
            }

            // USB 设备监控
            MonitorUsbDevice();

            Console.ReadKey();
        }
    }
}

