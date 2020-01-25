from django import forms


class CollectingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(CollectingForm, self).__init__(*args, **kwargs)

        self.initial['collect_from'] = 'all'
        self.initial['deduplication'] = 'not'

    key_words = forms.CharField(label="키워드", widget=forms.TextInput(
        attrs={'class': 'form-control',
               'autocomplete': 'off', 'data-role': 'tagsinput'}
    ))
    # collect_from = forms.ChoiceField(
    #     label="Collect From", choices=[('all', 'All (Title + Body)'), ('title', ' Title'), ('body', 'Body')], widget=forms.RadioSelect(
    #         attrs={'class': 'radio-inline'}
    #     ))
    # deduplication = forms.ChoiceField(
    #     label="Deduplication", choices=[('not', 'Not used'), ('url', 'URL based'), ('content', 'Content based')], widget=forms.RadioSelect)

    term = forms.CharField(label="기간", widget=forms.TextInput(
        attrs={
            'class': 'form-control', 'autocomplete': 'off'
        }
    ))
