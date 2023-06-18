from flask_definitions import *


@app.route("/<game_version>/catalog", methods=["GET"])
def catalog_get(game_version):
    print("Game Version of Catalog: " + game_version)
    get_remote_ip()
    try:
        return jsonify([
   {
      "Result":{
         "Id":"CompositeItemMetadata_0",
         "DisplayName":"Scavenger_SMOKE_Outfit_STR001_Black_NAME",
         "Purchasable":True,
         "Consumable":False,
         "IsWeapon":False,
         "InitialQuantity":1,
         "DefaultCost":{
            "CurrencyId":3,
            "Price":10
         },
         "EventCostList":{
            "Name":"Scavenger_SMOKE_Outfit_STR001_Black_NAME",
            "StartDate":1624038140,
            "EndDate":1718732540,
            "Cost":{
               "CurrencyId":3,
               "Price":10
            }
         },
         "MetaData":{
            "GameplayTags":{
               "TagName":"Class.Runner"
            },
            "BundleItems":[
               "RN_FOG_SMOKE_Head_STR004_Black_Item",
               "RN_FOG_SMOKE_UpperBody_STR004_Black_Item",
               "RN_FOG_SMOKE_LowerBody_STR004_Black_Item",
               "RN_FOG_SMOKE_Vambrace_STR004_Black_Item"
            ],
            "RewardBundleItems":[
               ""
            ],
            "RequiredChallangesToComplete":[
               ""
            ],
            "BundlePartOf":"",
            "PrerequisiteItem":"",
            "FollowingItem":"",
            "BundleDiscountPercent":69,
            "MinPlayerLevel":1,
            "MinCharacterLevel":1,
            "Origin":2
         },
         "Faction":2,
         "GameplayTagContainer":{
            "GameplayTags":{
               "TagName":"Runner.Smoke"
            },
            "ParentTags":{
               "TagName":"Customization.RN.FullSet"
            }
         },
         "CustomizationGameplayTagByFaction":[
            2,
            ""
         ],
         "Gender":0
      }
   }
])
    except TimeoutError:
        print("Timeout error")
        return jsonify({"status": "error"})
    except Exception as e:
        logger.graylog_logger(level="error", handler="unknown_catalog", message=str(e))


@app.errorhandler(404)
def debug_404(e):
    print("##################################################################################")
    print("DEBUG 404")
    print("##################################################################################")
    print('HTTP Headers:')
    for header in request.headers:
        print(f'{header[0]}: {header[1]}')

    print('Cookies:')
    for key, value in request.cookies.items():
        print(f'{key}: {value}')

    print('Endpoint: ', request.endpoint)
    print('Path: ', request.path)
    print('Method: ', request.method)

    if request.json:
        print('JSON Payload:')
        print(request.json)

    print("##################################################################################")
    return jsonify({"status": "error", "code": 404})
