from django.contrib import admin
from wmTippspiel.appWMTippspiel.models import Mannschaft, Begegnung, Tipps 


class BegegnungAdmin(admin.ModelAdmin):
    list_display = ('mannschaftHeim', 'mannschaftGast', 'toreHeim', 'toreGast', 'datum')
    search_fields = ('mannschaftHeim', 'mannschaftGast', 'datum')
    list_filter = ('datum',)
    date_hierarchy = 'datum'
    ordering = ('datum',)
    
    #Falls die Anzahl der Mannschaften zu viele werden
    #raw_id_fields = ('mannschaftHeim',)



class TippAdmin(admin.ModelAdmin):
    list_display = ('user', 'begegnung', 'toreHeim', 'toreGast', 'tippDatum')
    search_fields = ('user', 'tippDatum')
    list_filter = ('tippDatum',)
    date_hierarchy = 'tippDatum'
    ordering = ('tippDatum',)
    
    #Falls die Anzahl der Mannschaften zu viele werden
    #raw_id_fields = ('mannschaftHeim',)

admin.site.register(Mannschaft)
admin.site.register(Begegnung, BegegnungAdmin)
admin.site.register(Tipps, TippAdmin)
