/* SPDX-License-Identifier: GPL-2.0-or-later */
/**
 * acer-wmi-battery.c: Acer battery health control driver
 *
 * This is a driver for the WMI battery health control interface found
 * on some Acer laptops.  This interface allows to enable/disable a
 * battery charge limit ("health mode") and to calibrate the battery.
 */

#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/acpi.h>
#include <linux/wmi.h>

MODULE_DESCRIPTION("Acer battery health control driver");
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Frederik Harwath <frederik@harwath.name>");
#define WMI_GUID "79772EC5-04B1-4bfd-843C-61E7F77B6CC9"
MODULE_ALIAS("wmi:" WMI_GUID);

#ifdef pr_fmt
#undef pr_fmt
#define pr_fmt(fmt) "%s: " fmt, KBUILD_MODNAME
#endif

struct get_battery_health_control_status_input {
	u8 uBatteryNo;
	u8 uFunctionQuery;
	u8 uReserved[2];
} __packed;

struct get_battery_health_control_status_output {
	u8 uFunctionList;
	u8 uReturn[2];
	u8 uFunctionStatus[5];
} __packed;

struct set_battery_health_control_input {
	u8 uBatteryNo;
	u8 uFunctionMask;
	u8 uFunctionStatus;
	u8 uReservedIn[5];
} __packed;

struct set_battery_health_control_output {
	u8 uReturn;
	u8 uReservedOut;
} __packed;

enum battery_mode { HEALTH_MODE = 1, CALIBRATION_MODE = 2 };

struct battery_info {
	s8 health_mode;
	s8 calibration_mode;
};

static struct battery_info battery_status;

static short enable_health_mode = -1;

module_param(enable_health_mode, short, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);
MODULE_PARM_DESC(
	enable_health_mode,
	"Turn battery health mode on (value > 0) or off (value = 0) during module "
	"initialization (default value < 0: do not modify existing settings.)");

static acpi_status
get_battery_health_control_status(struct battery_info *bat_status)
{
	union acpi_object *obj;
	acpi_status status;

	/* Acer Care Center seems to always call the WMI method
	   with fixed parameters. This yields information about
	   the availability and state of both health and
	   calibration mode. The modes probably apply to
	   all batteries of the system - if there are
	   Acer laptops with multiple batteries? */
	struct get_battery_health_control_status_input params = {
		.uBatteryNo = 0x1,
		.uFunctionQuery = 0x1,
		.uReserved = { 0x0, 0x0 }
	};
	struct get_battery_health_control_status_output ret;

	struct acpi_buffer input = {
		sizeof(struct get_battery_health_control_status_input), &params
	};

	struct acpi_buffer output = { ACPI_ALLOCATE_BUFFER, NULL };

	status = wmi_evaluate_method(WMI_GUID, 0, 20, &input, &output);
	if (ACPI_FAILURE(status))
		return status;

	obj = output.pointer;
	if (!obj)
		return AE_ERROR;
	else if (obj->type != ACPI_TYPE_BUFFER) {
		kfree(obj);
		return AE_ERROR;
	}

	ret = *((struct get_battery_health_control_status_output *)
			obj->buffer.pointer);
	if (obj->buffer.length != 8) {
		pr_warn("Unknown buffer length %d\n", obj->buffer.length);
		kfree(obj);
		return AE_ERROR;
	}

	bat_status->health_mode = ret.uFunctionList & HEALTH_MODE ?
					  ret.uFunctionStatus[0] > 0 :
					  -1;
	bat_status->calibration_mode = ret.uFunctionList & CALIBRATION_MODE ?
					       ret.uFunctionStatus[1] > 0 :
					       -1;

	kfree(obj);

	return status;
}

static acpi_status set_battery_health_control(u8 function, bool function_status)
{
	union acpi_object *obj;
	acpi_status status;

	/* Cf. comment regarding constant argument values in
	   get_battery_health_control_status. */
	struct set_battery_health_control_input params = {
		.uBatteryNo = 0x1,
		.uFunctionMask = function,
		.uFunctionStatus = (u8)function_status,
		.uReservedIn = { 0x0, 0x0, 0x0, 0x0, 0x0 }
	};
	struct set_battery_health_control_output ret;

	struct acpi_buffer input = {
		sizeof(struct set_battery_health_control_input), &params
	};

	struct acpi_buffer output = { ACPI_ALLOCATE_BUFFER, NULL };
	status = wmi_evaluate_method(WMI_GUID, 0, 21, &input, &output);

	if (ACPI_FAILURE(status))
		return status;

	obj = output.pointer;

	if (!obj)
		return AE_ERROR;
	else if (obj->type != ACPI_TYPE_BUFFER) {
		kfree(obj);
		return AE_ERROR;
	}

	ret = *((struct set_battery_health_control_output *)obj->buffer.pointer);

	if (obj->buffer.length != 4) {
		pr_warn("Unknown buffer length %d\n", obj->buffer.length);
		kfree(obj);
		return AE_ERROR;
	}

	kfree(obj);

	return status;
}

static void print_modes(const char *prefix, bool print_if_empty,
			bool health_mode, bool calib_mode)
{
	if (!health_mode && !calib_mode && !print_if_empty)
		return;

	pr_info("%s modes: %s%s%s\n", prefix, health_mode ? "health mode" : "",
		health_mode && calib_mode ? ", " : "",
		calib_mode ? "calibration mode" : "");
}

static void init_state(void)
{
	bool print_state_if_empty;
	get_battery_health_control_status(&battery_status);

	print_state_if_empty = true;
	print_modes("available", print_state_if_empty,
		    battery_status.health_mode >= 0,
		    battery_status.calibration_mode >= 0);

	print_state_if_empty = false;
	print_modes("active", print_state_if_empty,
		    battery_status.health_mode > 0,
		    battery_status.calibration_mode > 0);
}

static void update_state(void)
{
	struct battery_info old_state = battery_status;
	get_battery_health_control_status(&battery_status);
	if (battery_status.calibration_mode != old_state.calibration_mode)
		pr_info("%s calibration mode\n",
			battery_status.calibration_mode ? "enabled" :
							  "disabled");
	if (battery_status.health_mode != old_state.health_mode)
		pr_info("%s health mode\n",
			battery_status.health_mode ? "enabled" : "disabled");
}

static ssize_t health_mode_show(struct device_driver *driver, char *buf)
{
	int len = sprintf(buf, "%d\n", battery_status.health_mode);
	if (len <= 0)
		pr_err("Invalid sprintf len: %d\n", len);

	return len;
}

static ssize_t health_mode_store(struct device_driver *driver, const char *buf,
				 size_t count)
{
	bool param_val;
	int err;
	if (battery_status.health_mode < 0)
		return 0;

	err = kstrtobool(buf, &param_val);
	if (err)
		return err;

	set_battery_health_control(HEALTH_MODE, param_val);

	return count;
}

static ssize_t calibration_mode_show(struct device_driver *driver, char *buf)
{
	int len = sprintf(buf, "%d\n", battery_status.calibration_mode);
	if (len <= 0)
		pr_err("Invalid sprintf len: %d\n", len);

	return len;
}

static ssize_t calibration_mode_store(struct device_driver *driver,
				      const char *buf, size_t count)
{
	bool param_val;
	int err;

	if (battery_status.calibration_mode < 0)
		return 0;

	err = kstrtobool(buf, &param_val);
	if (err)
		return err;

	set_battery_health_control(CALIBRATION_MODE, param_val);
	update_state();

	return count;
}

static DRIVER_ATTR_RW(health_mode);
static DRIVER_ATTR_RW(calibration_mode);

static struct attribute *acer_wmi_battery_attrs[] = {
	&driver_attr_health_mode.attr, &driver_attr_calibration_mode.attr, NULL
};

ATTRIBUTE_GROUPS(acer_wmi_battery);

static const struct wmi_device_id acer_wmi_battery_id_table[] = {
	{ .guid_string = WMI_GUID },
	{},
};

static struct wmi_driver acer_wmi_battery_driver = {
	.driver = { .name = "acer-wmi-battery",
		    .groups = acer_wmi_battery_groups },
};

static int __init acer_battery_init(void)
{
	if (!wmi_has_guid(WMI_GUID)) {
		pr_err("Acer battery control guid not found\n");
		return -ENODEV;
	}

	if (enable_health_mode >= 0)
		set_battery_health_control(HEALTH_MODE, enable_health_mode);
	init_state();

	return wmi_driver_register(&acer_wmi_battery_driver);
}

static void __exit acer_battery_exit(void)
{
	wmi_driver_unregister(&acer_wmi_battery_driver);
}

module_init(acer_battery_init);
module_exit(acer_battery_exit);
