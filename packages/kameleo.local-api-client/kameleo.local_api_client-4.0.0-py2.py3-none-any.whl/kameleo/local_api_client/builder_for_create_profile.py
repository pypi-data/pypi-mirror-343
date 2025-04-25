from typing import Optional, Union, IO

from kameleo.local_api_client._serialization import JSON


class BuilderForCreateProfile:
    def __init__(self, fingerprint_id):
        self.profile_request = self.reset(fingerprint_id)

    @staticmethod
    def for_fingerprint(fingerprint_id):
        if not fingerprint_id:
            raise ValueError("fingerprint_id must be set")
        return BuilderForCreateProfile(fingerprint_id)

    def build(self):
        result = self.profile_request
        self.profile_request = self.reset(result['fingerprintId'])
        return result

    def set_canvas(self, value):
        """Specifies how the canvas will be spoofed. Possible values:
            'intelligent': Use intelligent canvas spoofing. This will result non-unique canvas fingerprints.
            'noise': Add some noise to canvas generation.
            'block': Completely block the 2D API.
            'off': Turn off the spoofing, use the original settings.
        :param string value: Canvas spoofing type. Possible values: 'noise', 'block', 'off'
        """
        self.profile_request['canvas'] = value
        return self

    def set_webgl(self, value):
        """Specifies how the WebGL will be spoofed. Possible values:
            'noise': Add some noise to the WebGL generation
            'block': Completely block the 3D API
            'off': Turn off the spoofing, use the original settings.
        :param string value: WebGL spoofing type. Possible values: 'noise', 'block', 'off'
        """
        self.profile_request['webgl'] = value
        return self

    def set_webgl_meta(self, value, options):
        """Specifies how the WebGL vendor and renderer will be spoofed. Possible values:
            'automatic': The vendor and renderer values comes from the base profile.
            'manual': Manually set the vendor and renderer values.
            'off': Turn off the spoofing, use the original settings.
            :param string value: WebGLMeta spoofing type. Possible values: 'automatic', 'manual', 'off'
            :param options: When the WebglMeta spoofing is set to manual the webgl gpu vendor and renderer is required. For example: Google Inc. (NVIDIA)/ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)
            :type options: ~kameleo.local_api_client.models.WebglMetaSpoofingOptions
        """
        self.profile_request['webglMeta']['value'] = value
        self.profile_request['webglMeta']['extra'] = options
        return self

    def set_audio(self, value):
        """Specifies how the audio will be spoofed. Possible values:
            'noise': Add some noise to the Audio generation
            'block': Completely block the Audio API
            'off': Turn off the spoofing, use the original settings.
        :param string value: Audio spoofing type. Possible values: 'noise', 'block', 'off'
        """
        self.profile_request['audio'] = value
        return self

    def set_timezone(self, value, options):
        """Specifies how the timezone will be spoofed. Possble values:
            'automatic': Timezone is automatically set by the IP
            'manual': Timezone is manually overridden in the profile
            'off': Turn off the spoofing, use the original settings.
        :param string value: Timezone spoofing type. Possible values: 'automatic', 'manual', 'off'
        :param str options: When the Timezone spoofing is set to manual the timezone in Iana format is required. For example: America/Grenada
        """
        self.profile_request['timezone']['value'] = value
        self.profile_request['timezone']['extra'] = options
        return self

    def set_geolocation(self, value, options):
        """Specifies how the geolocation will be spoofed. Possible values:
            'automatic': Automatically set the values based on the IP address
            'manual': Manually set the longitude and latitude in the profile
            'block': Completely block the Geolocation API
            'off': Turn off the spoofing, use the original settings.
        :param string value: Geolocation spoofing type. Possible values: 'automatic', 'manual', 'block', 'off'
        :param options: When the Geolocation spoofing is set to manual the Geolocation coordinates must be provided
        :type options: ~kameleo.local_api_client.models.GeolocationSpoofingOptions
        """
        self.profile_request['geolocation']['value'] = value
        self.profile_request['geolocation']['extra'] = options
        return self

    def set_proxy(self, value, options):
        """Proxy connection settings of the profiles. Possible values:
            'none': Direct connection without any proxy.
            'http': Use a HTTP proxy for upstream communication.
            'socks5': Use a SOCKS5 proxy for upstream communication.
            'ssh': Use an SSH connection for upstream communication. Basically a SOCKS5 proxy created at the given SSH host.
        :param string value: Proxy connection type. Possible values: 'none', 'http', 'socks5', 'ssh'
        :param options: When the Proxy connection is set, a Proxy Server must be provided
        :type options: ~kameleo.local_api_client.models.Server
        """
        self.profile_request['proxy']['value'] = value
        self.profile_request['proxy']['extra'] = options
        return self

    def set_web_rtc(self, value, options):
        """Specifies how the WebRTC will be spoofed. Possible values:
            'automatic': Automatically set the webRTC public IP by the IP, and generates a random private IP like '2d2f78e7-1b1e-4345-a21b-07c904c98394.local'
            'manual': Manually override the webRTC public IP and private IP in the profile
            'block': Block the WebRTC functionality
            'off': Turn off the spoofing, use the original settings.
        :param string value: WebRTC spoofing type. Possible values: 'automatic', 'manual', 'block', 'off'
        :param options: When the WebRTC spoofing is set to manual, the private_ip and public_ip must be provided
        :type options: ~kameleo.local_api_client.models.WebRtcSpoofingOptions
        """
        self.profile_request['webRtc']['value'] = value
        self.profile_request['webRtc']['extra'] = options
        return self

    def set_fonts(self, value):
        """Specifies how the fonts will be spoofed. Possible values:
            'enabled': Enable fonts spoofing.
            'disable': Disable fonts spoofing.
        :param string value: Fonts spoofing type. Possible values: 'enabled', 'disabled'
        """
        self.profile_request['fonts'] = value
        return self

    def set_start_page(self, value):
        """This website will be opened in the browser when the profile launches.
        :param string value: The url of the start page
        """
        self.profile_request['startPage'] = value
        return self

    def set_password_manager(self, value):
        """Enable or disable the password manager function in the browser. Possible values:
            'enabled': Enable password manager so browser will ask to save and load passwords on logins.
            'disable': Disable password manager.
        :param string value: Password Manager possible values: 'enabled', 'disabled'
        """
        self.profile_request['passwordManager'] = value
        return self

    def set_screen(self, value, options):
        """Specifies how the screen will be spoofed. Possible values:
            'automatic': Automatically override the screen resolution based on the Base Profile.
            'manual': Manually override the screen resolution.
            'off': Turn off the spoofing, use the original settings.
        :param string value: Screen spoofing type. Possible values: 'automatic', 'manual', 'off'
        :param string options: When the Screen spoofing is set to manual, the required screen size must be provided. For example: 1080x1920
        """
        self.profile_request['screen']['value'] = value
        self.profile_request['screen']['extra'] = options
        return self

    def set_extensions(self, absolute_paths):
        """A list of absolute paths from where the profile should load extensions or addons when starting the browser. For chrome and edge use CRX3 format extensions. For firefox use signed xpi format addons.
        :param absolute_paths: A list of abolute paths from where the profile should load extensions or addons when starting the browser.
        :type absolute_paths: list[str]
        """
        self.profile_request['extensions'] = absolute_paths
        return self

    def set_notes(self, notes):
        """A free text including any notes written by the user.
        """
        self.profile_request['notes'] = notes
        return self

    def set_name(self, name):
        """Sets the name of the profile.
        """
        self.profile_request['name'] = name
        return self

    def set_tags(self, tags):
        """Sets the tags of the profile.
        """
        self.profile_request['tags'] = tags
        return self

    def set_hardware_concurrency(self, value, options):
        """Specifies how the hardwareConcurrency will be spoofed. Possible values:
        'automatic': Automatically override the hardwareConcurrency based on the Base Profile.
        'manual': Manually override the hardwareConcurrency.
        'off': Turn off the spoofing, use the original settings.
        :param int value: HardwareConcurrency spoofing type. Possible values: 'automatic', 'manual', 'off'
        :param int options: When the HardwareConcurrency spoofing is set to manual, the required value must be provided.
        Valid values: 1,2,4,8,16.
        """
        self.profile_request['hardwareConcurrency']['value'] = value
        self.profile_request['hardwareConcurrency']['extra'] = options
        return self

    def set_device_memory(self, value, options):
        """Specifies how the deviceMemory will be spoofed. Possible values:
            'automatic': Automatically override the deviceMemory based on the Base Profile.
            'manual': Manually override the deviceMemory. Valid values: 0.25, 0.5, 1, 2, 4, 8.
            'off': Turn off the spoofing, use the original settings.
        :param string value: DeviceMemory spoofing type. Possible values: 'automatic', 'manual', 'off'
        :param double options: When the DeviceMemory spoofing is set to manual, the required value must be provided.
        Valid values: 0.25, 0.5, 1, 2, 4, 8.
        """
        self.profile_request['deviceMemory']['value'] = value
        self.profile_request['deviceMemory']['extra'] = options
        return self


    def set_launcher(self, browser_launcher):
        """The mode how the profile should be launched. It determines which browser to launch. This cannot be modified after creation.
            Possible values for Desktop profiles 'automatic'.
            Possible values for Mobile profiles: 'chromium', 'external'.
        :param string browser_launcher: Browser Launcher. Possible values: 'automatic', 'external'
        """
        self.profile_request['launcher'] = browser_launcher
        return self

    def set_recommended_defaults(self):
        """This sets all the profile options to the defaults recommended by Kameleo Team. Please consider providing Proxy settings to your profile.
        """
        self.profile_request['canvas'] = "intelligent"
        self.profile_request['webgl'] = "off"
        self.profile_request['webglMeta']['value'] = "automatic"
        self.profile_request['audio'] = "off"
        self.profile_request['timezone']['value'] = "automatic"
        self.profile_request['geolocation']['value'] = "automatic"
        self.profile_request['webRtc']['value'] = "automatic"
        self.profile_request['fonts'] = "enabled"
        self.profile_request['screen']['value'] = "automatic"
        self.profile_request['hardwareConcurrency']['value'] = "automatic"
        self.profile_request['deviceMemory']['value'] = "automatic"
        self.profile_request['launcher'] = "automatic"
        self.profile_request['startPage'] = "about:newtab"

        return self

    def reset(self, fingerprint_id) -> Optional[Union[JSON, IO]]:
        data = {
            "fingerprintId": fingerprint_id,
            "canvas": "off",
            "webgl": "off",
            "webglMeta": {
                "value": "off",
                "extra": None
            },
            "audio": "off",
            "timezone": {
                "value": "off",
                "extra": None
            },
            "geolocation": {
                "value": "off",
                "extra": None
            },
            "proxy": {
                "value": "none",
                "extra": None
            },
            "webRtc": {
                "value": "off",
                "extra": None
            },
            "fonts": "disabled",
            "screen": {
                "value": "off",
                "extra": None
            },
            "hardwareConcurrency": {
                "value": "off",
                "extra": None
            },
            "deviceMemory": {
                "value": "off",
                "extra": None
            },
            "passwordManager": "disabled"
        }
        return data
