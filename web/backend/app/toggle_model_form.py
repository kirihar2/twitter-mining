class ToggleModelForm(forms.ModelForm):
    class Meta:
        model = GPIO
        fields = ('GPIO_Pin', 'toggle_on','pub_date') #Note that we didn't mention user field here.

    def save(self, gpio=None):
        gpio_pin = super(ToggleModelForm, self).save(commit=False)
        if gpio:
            gpio_pin.GPIO_Pin = gpio
        gpio_pin.save()
        return gpio_pin