# Lidl Plus – API-Dokumentation (Android 17.11.4)

> Statisch aus der APK rekonstruiert (jadx + eigener Hermes-v96-String-Parser). Kein Live-Traffic geprüft. Basis-URLs sind die **Produktions**-Umgebung; zu fast allen gibt es `-uat`/`-stg`-Varianten. Host-Zuordnung pro Modul ist aus Modulnamen und Environment-Config-Klassen abgeleitet, bei mit `?` markierten nicht eindeutig.

## 1. Authentifizierung (OIDC / OAuth2 + PKCE)

| | |
|---|---|
| Issuer | `https://accounts.lidl.com/` |
| Authorize | `GET https://accounts.lidl.com/connect/authorize` |
| Token | `POST https://accounts.lidl.com/connect/token` |
| End-Session | `GET https://accounts.lidl.com/connect/endsession` (`id_token_hint`, `post_logout_redirect_uri`, `state`) |
| Nonce | `POST https://accounts.lidl.com/connect/nonce` |
| client_id | `LidlPlusNativeClient` (Public Client, kein Secret) |
| response_type | `code`, PKCE `S256` |
| scope | `openid profile offline_access lpprofile lpapis` |
| redirect_uri | `com.lidlplus.app://callback` |
| Zusätzliche Authorize-Parameter | `Country=<CC>`, `language=<lang>-<CC>` (z. B. `de-DE`), `force=<bool>`, `track=<bool>` |

Token-Request: `grant_type=authorization_code` bzw. `refresh_token`, `client_id=LidlPlusNativeClient`, `code_verifier`, `redirect_uri`.
Access-Token wird als `Authorization: Bearer <token>` gesendet; Refresh über `offline_access`.

Weitere Account-Seiten (WebView): `account/email`, `account/phone`, `profile/security`, `account/login/mobile?client_id=LidlPlusNativeClient`.

Daneben existiert ein Web-Login für E-Commerce: `https://accounts.lidl.com/account/login/browser?client_id=lidlappclient&country_code=..&language=..&track=..&redirect_uri=..`.

## 2. Gemeinsame Header (OkHttp-Interceptor)

| Header | Wert |
|---|---|
| `Authorization` | `Bearer <access_token>` (eingeloggte Endpunkte) |
| `App` | `com.lidl.eci.lidlplus` |
| `App-Version` | App-Version, z. B. `17.11.4` |
| `Operating-System` | `Android` |
| `Accept-Language` | `<lang>-<CC>`, z. B. `de-DE` |
| `Segment-Ids` | (einige Endpunkte) Nutzersegmente, kommasepariert |
| `UserLevel` | (Home) Loyalty-Level |
| `Firebase-Installations` | (Push) |
| `Sdk-Version` / `Use-Canary` | Payments-SDK (`8.7.6`) |

`{country}` / `{countryCode}` / `{countryId}` = ISO-3166 Alpha-2, meist Großbuchstaben (`DE`).

## 3. Hosts (Prod)

| Modul | Basis-URL |
|---|---|
| alerts | `https://alerts.lidlplus.com/api/` |
| announcements | `https://announcements.lidlplus.com/api/` |
| app-update | `https://versions.lidlplus.com/` |
| authentication-web | `https://accounts.lidl.com/` |
| benefits | `https://stampcardbenefits.lidlplus.com/api/` |
| branddeals-ads | `https://branddeals.lidlplus.com/api/` |
| brochures | `https://brochures.lidlplus.com/` |
| clickandpick | `https://clickandpick.lidlplus.com/` |
| collectionmodel | `https://mypoints.lidl.com/mobile-bff/` |
| commons-configuration | `https://appgateway.lidlplus.com/configurationapp/` |
| commons-literalsprovider | `https://localization.lidlplus.com/resources/` |
| commons-user | `https://segments.lidlplus.com/` |
| commons-user-model | `https://usermodel.lidlplus.com/` |
| consent | `https://consent.lidlplus.com/api/` |
| contentpartners | `https://subscriptions.lidlplus.com/app-api/` |
| coupid | `https://coupid.lidlplus.com/` |
| couponplus | `https://couponplus.lidlplus.com/api/` |
| coupons | `https://coupons.lidlplus.com/app/api/  (Tracking: /app/api/tracking/, absolute Pfade ab Host-Root)` |
| deposits | `https://deposits.lidlplus.com/api/` |
| digitalleaflet | `https://digital-leaflet.lidlplus.com/` |
| ecommerce | `https://www.lidl.{tld}/  (teilw. https://live.api.schwarz/, recommendations.lidl-shop.com, Criteo)` |
| emobilitySDK_release | `https://emobility.lidl.com/` |
| employee-benefits | `https://employeeprogram.lidlplus.com/` |
| flashsales | `https://flashsales.lidlplus.com/api/` |
| frederix | `(dynamisch / Health-Check)` |
| grocerypickup | `https://grocerypickup.lidlplus.com/` |
| home | `https://home.lidlplus.com/api/ bzw. /configuration/` |
| integration | `https://worldofneeds.lidlplus.com/` |
| inviteyourfriends | `https://inviteyourfriends.lidlplus.com/api/` |
| lib_release | `https://eventtracker.dsa.apps.schwarz/` |
| libs-tracking-adobe-experience | `https://eventtracker.dsa.apps.schwarz/ / https://myip.lidlplus.com/` |
| libs-unleash | `https://unleash-mobile.scrm.apps.schwarz/` |
| lidlplusPaymentsSDK | `https://eticket.lidlplus.com/` |
| lottery | `https://stampcard.lidlplus.com/api/` |
| loyalty | `(Loyalty-Cards-Service, Host dynamisch)` |
| metahome | `https://home.lidlplus.com/api/ bzw. /configuration/` |
| offers | `https://offers.lidlplus.com/app/api/` |
| opengift | `https://opengift.lidlplus.com/api/` |
| paymentsSDK | `https://payments.lidlplus.com/` |
| personalisedsurveys | `https://persosurveys.lidlplus.com/client/api/` |
| productcatalog | `https://product-catalog.lidlplus.com/` |
| products-featured | `https://productshowcase.lidlplus.com/featured/` |
| products-recommended | `https://productshowcase.lidlplus.com/recommended/` |
| products-related | `https://productshowcase.lidlplus.com/related/` |
| productshowcase | `https://productshowcase.lidlplus.com/` |
| profile | `https://devices.lidlplus.com/api/` |
| profile-user | `https://profile.lidlplus.com/api/` |
| purchaselottery | `https://purchaselottery.lidlplus.com/api/` |
| purchasesummary | `https://summary.lidlplus.com/api/` |
| push | `https://push-notifications.lidlplus.com/` |
| rewards | `https://stampcard.lidlplus.com/api/` |
| shortcut | `https://home.lidlplus.com/configuration/` |
| stores | `https://stores.lidlplus.com/api/` |
| surveys | `https://surveys.lidlplus.com/api/` |
| thirdpartybenefit | `https://partnersbenefits.lidlplus.com/app/` |
| tickets | `https://tickets.lidlplus.com/api/` |
| tipcards | `https://tipcards.lidlplus.com/api/` |
| travel | `https://travel.lidlplus.com/api/` |
| uniqueaccount | `https://aboutme.lidl.com/` |
| worldofneeds | `https://worldofneeds.lidlplus.com/` |
| wrapped | `https://wrapped.lidlplus.com/` |

Weitere Hosts (nur in Config/Webviews/RN): `profile.lidl.com`, `preferencecenter.lidl.com`, `mylidlaccount.lidl.com`, `familyclub.lidl.com`, `selfscanning.lidlplus.com/api/`, `storetools.lidlplus.com/api/`, `giveaway.lidlplus.com/api/`, `personalized-campaigns.lidlplus.com/`, `shopping-list.lidlplus.com/api`, `connect.lidlplus.com/app-api`, `badges.lidl.com`, `status.lidl.com`, `recipes-core-api-stackit.recipes.lidl`, `mobile-otel.lidlplus.com:4417/v1/traces` (OpenTelemetry).

## 4. Native Endpunkte (Retrofit, 343 Endpunkte in 117 Interfaces)

Legende Parameter: `P` = Path, `Q` = Query, `H` = Header, `B` = JSON-Body, `F` = Form-Field, `Pt` = Multipart-Part, `U` = volle URL.

### alerts
Basis: `https://alerts.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `v1/{country}/alerts/pending` | B:`PendingAlertsRequestModel` | `(leer)` |
| `DELETE` | `v2/{country}` | H:`Accept-Language`, H:`Segment-Ids` | `DeleteAllAlertsModel` |
| `GET` | `v2/{country}` | H:`Accept-Language`, H:`Segment-Ids`, H:`isOneApp` | `List<AlertModel>` |
| `GET` | `v2/{country}/alerts/unread` | H:`Accept-Language`, H:`Segment-Ids`, H:`isOneApp` | `UnreadAlertModel` |
| `DELETE` | `v2/{country}/alerts/{alertId}` | H:`Accept-Language`, H:`Segment-Ids` | `DeleteAlertModel` |
| `POST` | `v3/{country}/alerts/{alertId}/read` | H:`Accept-Language`, H:`Segment-Ids` | `ReadAlertModel` |

### announcements
Basis: `https://announcements.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `v1/{country}/viewed` | B:`AnnouncementViewedRequest` | `(leer)` |
| `GET` | `v2/{country}` | H:`Accept-Language`, H:`Store-Id`, H:`Segment-Ids`, H:`isOneApp`, H:`Section` | `List<AnnouncementModel>` |

### app-update
Basis: `https://versions.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{country}/init` | Q:`AttributionReporter.APP_VERSION`, Q:`os`, H:`DeviceId`, H:`Accept-Language`, H:`Operating-System`, H:`Model`, H:`Brand` | `uk3<Response>` |

### authentication-web
Basis: `https://accounts.lidl.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `connect/nonce` | H:`Authorization`, F:`token` form-urlencoded | `yij` |

### benefits
Basis: `https://stampcardbenefits.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v3/{country}/user/promotions` | Q:`storeId` | `StampCardBenefitsModel` |
| `PATCH` | `v3/{country}/user/promotions/{id}/cards/viewed` | B:`List<UUID>` | `(leer)` |
| `GET` | `v3/{country}/user/promotions/{id}/congrats` |  | `CongratulationsModel` |
| `GET` | `v3/{country}/user/promotions/{id}/detail` |  | `DetailModel` |
| `PATCH` | `v3/{country}/user/promotions/{id}/started` |  | `(leer)` |

### branddeals-ads
Basis: `https://branddeals.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `/api/v2/{countryCode}/ad/{adId}/clicks` | B:`DispatchEventBody`, Q:`correlationId` | `(leer)` |
| `POST` | `v3/{countryCode}/ad/{adId}/impressions` | B:`DispatchEventBody`, Q:`correlationId` | `(leer)` |
| `POST` | `v3/{countryCode}/ad/{adId}/views` | B:`DispatchEventBody`, Q:`correlationId` | `(leer)` |
| `GET` | `v3/{countryCode}/ads` | H:`Accept-Language`, Q:`AdRevenueScheme.PLACEMENT` | `BrandDealsSessionResponse` |
| `POST` | `v3/{countryCode}/ads/{adId}/claim/{promotionId}/{adTemplateId}` | B:`ClaimEventBody` | `CouponCard` |

### brochures
Basis: `https://brochures.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/v2/{country}/Brochures` | Q:`Payload.TYPE_STORE` | `List<FlyerCategory>` |

### clickandpick
Basis: `https://clickandpick.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `DELETE` | `api/v1/clickandpick/{countryId}/order` | H:`Accept-Language` | `(leer)` |
| `GET` | `api/v1/clickandpick/{countryId}/order` | H:`Accept-Language` | `ClickandpickOrderResponseModel` |
| `PATCH` | `api/v1/clickandpick/{countryId}/order` | H:`Accept-Language` | `(leer)` |
| `GET` | `api/v1/clickandpick/{countryId}/stores/{storeId}/cart` | H:`Accept-Language` | `ClickandpickCartCartResponseModel` |
| `POST` | `api/v1/clickandpick/{countryId}/stores/{storeId}/cart/checkout` | H:`Accept-Language`, B:`ClickandpickCartCheckoutRequestModel` | `(leer)` |
| `PATCH` | `api/v1/clickandpick/{countryId}/stores/{storeId}/cart/product/{id}` | H:`Accept-Language`, B:`ClickandpickCartAddProductRequestModel` | `ClickandpickCartCartResponseModel` |
| `POST` | `api/v1/clickandpick/{countryId}/stores/{storeId}/cart/product/{id}` | H:`Accept-Language`, B:`ClickandpickCartAddProductRequestModel` | `ClickandpickCartAddProductResponseModel` |
| `GET` | `api/v1/clickandpick/{countryId}/stores/{storeId}/products` | H:`Accept-Language` | `ClickandpickListResponseModel` |
| `GET` | `api/v1/clickandpick/{countryId}/stores/{storeId}/products/{id}` | H:`Accept-Language` | `ClickandpickProductModel` |
| `GET` | `api/v2/clickandpick/{countryId}/stores/{storeId}/campaign/status` |  | `ClickandpickCampaignResponseModel` |

### collectionmodel
Basis: `https://mypoints.lidl.com/mobile-bff/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `DELETE` | `api/v1/{countryCode}/favorite/{rewardId}` | H:`UserLevel` | `(leer)` |
| `PUT` | `api/v1/{countryCode}/favorite/{rewardId}` | H:`UserLevel` | `(leer)` |
| `GET` | `api/v1/{countryCode}/onboarding` | Q:`storeId`, H:`Segment-Ids` | `OnBoardingDTO` |
| `POST` | `api/v1/{countryCode}/onboarding` | Q:`storeId`, H:`Segment-Ids` | `OnboardingCompletedDTO` |
| `GET` | `api/v1/{countryCode}/userReward/undo` | Q:`rewardId`, Q:`userPromotionId` | `UndoRewardDataDTO` |
| `POST` | `api/v1/{countryCode}/userReward/undo` | B:`UndoRewardBody` | `(leer)` |
| `GET` | `api/v1/{countryCode}/userpoints/{userId}` |  | `UserPoints` |
| `GET` | `api/v10/{countryCode}/marketplace/all` | Q:`languageCode`, Q:`storeId`, Q:`page`, Q:`sortBy`, Q:`include`, Q:`filter[points-min]`, Q:`filter[points-max]`, Q:`filter[categories]`, Q:`quickCategory`, H:`Segment-Ids`, Q:`withPreviousPages`, H:`UserLevel` | `MarketPlaceDTO` |
| `POST` | `api/v2/{countryCode}/exchange/{rewardId}` | Q:`storeId`, H:`Segment-Ids`, H:`UserLevel` | `(leer)` |
| `GET` | `api/v2/{countryCode}/freepoints/campaign/{campaignID}` | Q:`languageCode`, H:`Segment-Ids` | `CampaignDetailDTO` |
| `GET` | `api/v2/{countryCode}/summary` | H:`Segment-Ids` | `SummaryDTO` |
| `GET` | `api/v3/{countryCode}/freepoints/all` | Q:`languageCode`, Q:`storeId`, H:`Segment-Ids` | `FreePointsDTO` |
| `GET` | `api/v7/{countryCode}/marketplace/id/{id}` | Q:`languageCode`, Q:`storeId`, H:`Segment-Ids`, H:`UserLevel` | `RewardDetailDTO` |

### commons-configuration
Basis: `https://appgateway.lidlplus.com/configurationapp/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v3/countries` | H:`isBeta` | `List<LidlPlusConfigurationAppApiFeaturesGetCountriesV3ModelsCountryResponse>` |
| `GET` | `v3/countryconfigurations/{countryCode}` | Q:`storeId`, Q:`firebaseConfigs`, Q:`segmentIds`, H:`isBeta` | `LidlPlusConfigurationAppApiFeaturesGetCountryConfigurationByStoreV3CountryConfigurationModel` |

### commons-literalsprovider
Basis: `https://localization.lidlplus.com/resources/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/resources/{country}/{language}` | Q:`resourceType`, Q:`version` | `LocalizationResponse` |

### commons-user
Basis: `https://segments.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/v1/usersegments/{countryCode}` |  | `List<String>` |

### commons-user-model
Basis: `https://usermodel.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/v1/usermodel/{countryCode}` |  | `Map<String, wpf>` |

### consent
Basis: `https://consent.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `v4/{country}/evidence/storeevidence` | H:`Authorization`, B:`ConsentBodyRequest` | `(leer)` |

### contentpartners
Basis: `https://subscriptions.lidlplus.com/app-api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{countryCode}/billinginfo` |  | `wh2` |
| `POST` | `v1/{countryCode}/checkout/{partnerId}` | B:`wvl` | `zvl` |
| `POST` | `v1/{countryCode}/events/track` | B:`fhv` | `(leer)` |
| `GET` | `v1/{countryCode}/marketplace` | H:`Segment-Ids` | `yzh` |
| `GET` | `v1/{countryCode}/partners` |  | `List<q2l>` |
| `GET` | `v1/{countryCode}/partners/minified` |  | `List<j2l>` |
| `PUT` | `v1/{countryCode}/paymentConfiguration/plans/{partnerId}/paymentMethod` | B:`cal` | `(leer)` |
| `GET` | `v1/{countryCode}/planManager` |  | `oul` |
| `PATCH` | `v1/{countryCode}/planManager/gamification` | B:`oew` | `(leer)` |
| `GET` | `v1/{countryCode}/plans/{partnerId}` |  | `ksl` |
| `PUT` | `v1/{countryCode}/plans/{partnerId}/cancel` |  | `(leer)` |
| `PUT` | `v1/{countryCode}/plans/{partnerId}/cancelform` | B:`o44` | `o24` |
| `POST` | `v1/{countryCode}/plans/{partnerId}/connect` | B:`u86` | `x86` |
| `GET` | `v1/{countryCode}/plans/{partnerId}/update-info` |  | `uwl` |
| `POST` | `v3/{countryCode}/checkout` | B:`x05` | `a15` |
| `POST` | `v3/{countryCode}/transactions/creation` | H:`Accept`, B:`ujv` | `dkv` |
| `POST` | `v3/{countryCode}/transactions/update` | H:`Accept`, B:`pyl` `User-Agent: Lidl/+ Android` | `dkv` |
| `POST` | `v4/{countryCode}/transactions/confirmation` | B:`kjv` | `pjv` |

### coupid
Basis: `https://coupid.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `/play/v1/game/status` | H:`Authorization`, H:`Accept`, H:`X-User-Segments`, Q:`countryCode` | `ResponseBody (raw)` |

### couponplus
Basis: `https://couponplus.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v4/{country}/user/promotions` | H:`Segment-Ids` | `CouponPlusApiModel` |
| `PATCH` | `v4/{country}/user/promotions/{id}/goals/view` |  | `(leer)` |
| `PATCH` | `v4/{country}/user/promotions/{id}/start` | H:`Segment-Ids` | `(leer)` |

### coupons
Basis: `https://coupons.lidlplus.com/app/api/  (Tracking: /app/api/tracking/, absolute Pfade ab Host-Root)`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `/user-activity-api/v1/users/activity` | Q:`country` | `(leer)` |
| `GET` | `v1/promotionscount` | H:`Accept-Language`, H:`Country`, H:`Segment-Ids` | `ActivePromotionsCount` |
| `POST` | `v1/{country}/promotionviewevents` | B:`List<PromotionEventModel>` | `(leer)` |
| `GET` | `v2/promotions/titles` | H:`country`, Q:`ids`, H:`Accept-Language` | `List<PromotionTitleModel>` |
| `DELETE` | `v2/promotions/{id}/activation` | H:`Country`, H:`Accept-Language`, H:`Action-Location` | `(leer)` |
| `POST` | `v2/promotions/{id}/activation` | H:`Country`, H:`Accept-Language`, B:`ArticleSelection`, H:`Action-Location`, H:`UserLevel` | `(leer)` |
| `PATCH` | `v4/overrides/discount/{id}` | H:`country`, H:`Accept-Language`, H:`Action-Location`, B:`ArticleSelection` | `(leer)` |
| `GET` | `v4/promotions/cards` | H:`country`, Q:`ids`, H:`Accept-Language`, H:`UserLevel` | `List<PromotionCardModel>` |
| `GET` | `v4/promotionsbyarticle` | Q:`ArticleIds`, Q:`CategoryIds`, Q:`RedemptionChannel`, H:`Accept-Language`, H:`Country`, H:`Segment-Ids` | `PromotionsByArticleResponseModel` |
| `GET` | `v4/promotionsbyarticle/anonymous` | Q:`ArticleIds`, Q:`CategoryIds`, Q:`RedemptionChannel`, H:`Accept-Language`, H:`Country` | `PromotionsByArticleResponseModel` |
| `GET` | `v4/promotionsdetails/{id}` | H:`Country`, H:`Accept-Language`, H:`Segment-Ids`, H:`UserLevel` | `PromotionDetailModel` |
| `GET` | `v4/promotionslist` | H:`Accept-Language`, H:`Country`, H:`Segment-Ids`, H:`Store-Id`, H:`UserLevel`, H:`World`, H:`Tags` | `PromotionListModel` |
| `GET` | `v4/promotionslist/anonymous` | H:`Accept-Language`, H:`Country`, H:`Store-Id`, H:`World`, H:`Tags` | `PromotionListModel` |

### deposits
Basis: `https://deposits.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{country}/deposit/{depositId}` |  | `DepositDetailResponse` |
| `PATCH` | `v1/{country}/deposit/{depositId}/status` | B:`String` | `(leer)` |
| `GET` | `v1/{country}/deposit/{depositId}/summary` |  | `DepositSummaryResponse` |
| `GET` | `v1/{country}/deposits` |  | `DepositsResponse` |
| `POST` | `v1/{country}/identification` | B:`RVMRequest` | `(leer)` |
| `PUT` | `v1/{country}/settings` | B:`SettingsRequest` | `(leer)` |

### digitalleaflet
Basis: `https://digital-leaflet.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/v1/{countryId}/campaignGroups` | Q:`storeId`, Q*:`Map<String, Boolean>` | `DigitalLeafletResponseCampaignGroupsModel` |
| `GET` | `api/v1/{countryId}/campaigns/{campaignId}` | Q*:`Map<String, Boolean>`, Q:`storeId` | `DigitalLeafletResponseCampaignDetailModel` |
| `GET` | `api/v1/{countryId}/products/{productId}` | Q*:`Map<String, Boolean>`, Q:`storeId`, Q:`discardOnline` | `DigitalLeafletResponseProductDetailModel` |
| `POST` | `api/v1/{countryId}/useractivity` | B:`DigitalLeafletRequestPostUserActivityModel` | `(leer)` |

### ecommerce
Basis: `https://www.lidl.{tld}/  (teilw. https://live.api.schwarz/, recommendations.lidl-shop.com, Criteo)`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `(@Url)` | U:`String` | `(leer)` |
| `GET` | `(@Url)` | U:`String`, H:`x-myra-traffic-bucket` | `vji` |
| `GET` | `/c/api/content-pages/{contentPageId}/{countryCode}/{languageCode}` |  | `yh6` |
| `GET` | `/c/api/shop_the_look_component/{locale}` | Q:`productId` | `icr` |
| `GET` | `/c/api/shop_the_look_slider_component/{locale}` | Q:`shopTheLookIds` | `List<icr>` |
| `GET` | `/n/disclaimer-text/{disclaimerValue}` |  | `gc9` |
| `GET` | `/n/navigation-marketing-message` |  | `fwh` |
| `GET` | `/n/pdp-layers` | Q:`country` | `tdl` |
| `GET` | `/p/api/detail/{productErp}/{countryCode}/{languageCode}` |  | `eim` |
| `GET` | `/p/api/digital/general-terms/{brandId}/{country}/{language}` |  | `String` |
| `GET` | `/p/api/digital/redemption-conditions/{brandId}/{country}/{language}` |  | `String` |
| `GET` | `/p/api/gridboxes/{countryCode}/{languageCode}` | Q:`erpNumbers`, Q:`max` | `List<i3n>` |
| `POST` | `/p/api/mobile/back-in-stock/subscribe/{countryCode}/{languageCode}` | Q:`token`, Q:`erp`, Q:`deviceId`, Q:`ssoId`, Q:`captchaToken`, Q:`zone` | `tp1` |
| `GET` | `/p/api/mobile/back-in-stock/subscriber` |  | `xit` |
| `POST` | `/p/api/mobile/back-in-stock/unsubscribe/{countryCode}/{languageCode}` | Q:`token`, Q:`erp`, Q:`deviceId`, Q:`ssoId`, Q:`captchaToken`, Q:`reason`, Q:`zone` | `tp1` |
| `GET` | `/p/api/shopthelook/{country}/{language}` | Q:`erpNumbers` | `Map<String, gdr>` |
| `GET` | `/prbs-api/aplazame/minRate` | Q:`amount` | `Double` |
| `GET` | `/u/api/product/{productErp}/{countryCode}/{languageCode}` |  | `p6o` |
| `POST` | `/user-api/get-session` | B:`wgp`, Q:`key` | `tvc` |
| `GET` | `c/api/campaigns/{campaignId}/{countryCode}/{languageCode}` |  | `kv3` |
| `GET` | `category/h/{category}?version=v2.0.0` | Q:`assortment`, Q:`RegistrationDbStorage.Columns.LOCALE`, Q:`offset`, Q:`fetchsize`, H:`x-myra-traffic-bucket` | `vji` |
| `GET` | `delivery/retailmedia` | Q*:`Map<String, String>` | `(leer)` |
| `GET` | `delivery/retailmedia?event-type=viewItem&page-id=viewItemApiAa` | Q:`criteo-partner-id`, Q:`retailer-visitor-id`, Q:`customer-id`, Q:`email`, Q:`item`, Q:`price`, Q:`availability`, Q:`parent-item` | `pm7` |
| `GET` | `delivery/retailmedia?event-type=viewSearchResult&page-id=viewSearchResultApiAa` | Q:`criteo-partner-id`, Q:`retailer-visitor-id`, Q:`customer-id`, Q:`email`, Q:`item`, Q:`keywords`, Q:`list-size`, Q:`page-number`, Q:`parent-item` | `pm7` |
| `POST` | `oauth/accesstoken` | F:`grant_type`, F:`client_id`, F:`client_secret` form-urlencoded | `t9` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/bestsellers` | Q:`limit`, Q:`brandViewedProducts` | `xx2` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/bestsellers` | Q:`limit`, Q:`categoryIds`, Q:`campaignIds`, Q:`brandIds`, Q:`onSale`, Q:`omnichannel` | `xx2` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/bestsellers` | Q:`limit`, Q:`categoryViewedProducts` | `xx2` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/bundles/{productId}` | Q:`limit` | `njo` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/cross/{erpNumber}` | Q:`limit` | `njo` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/customers` | Q:`limit`, Q:`ssoId` | `njo` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/marketingmessage` | Q:`ssoId`, Q:`zone` | `tkl` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/multicross` | Q:`limit`, Q:`antecedents` | `njo` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/products/{erpNumber}` | Q:`limit` | `njo` |
| `GET` | `r/api/recommendations/{countryCode}/{languageCode}/web/shopthelook` | Q:`pageType`, Q:`pageId`, Q:`limit` | `zgp` |
| `GET` | `search?version=v2.0.0` | Q:`Constants.ScionAnalytics.PARAM_CAMPAIGN`, Q:`assortment`, Q:`RegistrationDbStorage.Columns.LOCALE`, Q:`offset`, Q:`fetchsize`, Q:`online`, H:`x-myra-traffic-bucket` | `vji` |
| `GET` | `search?version=v2.0.0` | Q:`RegistrationDbStorage.Columns.LOCALE`, Q:`q`, Q:`assortment`, Q:`offset`, Q:`fetchsize`, H:`x-myra-traffic-bucket` | `vji` |
| `POST` | `sit/autodispolidl/store-stock/v2/stocks/country/{countryCode}/search-by-products` | Q:`business-date`, B:`d4n` | `List<w9n>` |
| `GET` | `sit/autodispolidl/store-stock/v2/stocks/country/{countryCode}/store/{storeNumber}/product/{productId}` | Q:`business-date` | `w9n` |
| `POST` | `sit/autodispolidl/store-stock/v2/variant-stocks/country/{countryCode}/search-by-product-or-variant` | Q:`product`, Q:`business-date`, B:`List<String>` | `List<a0x>` |
| `GET` | `sit/checkout-pca/cart-api/v1/cart-api/order/{cartId}` |  | `phk` |
| `POST` | `sit/checkout-pca/cart-api/v1/cart-api/salesforce/events/{country}/{externalKey}` | B:`c2` | `(leer)` |
| `DELETE` | `sit/checkout-pca/cart-api/v1/cart-api/v2/cart` | H:`Cookie`, H:`x-myra-traffic-bucket`, Q:`erpNumber` | `li4` |
| `GET` | `sit/checkout-pca/cart-api/v1/cart-api/v2/cart` | H:`Cookie`, H:`x-myra-traffic-bucket` | `li4` |
| `PATCH` | `sit/checkout-pca/cart-api/v1/cart-api/v2/cart` | H:`Cookie`, H:`x-myra-traffic-bucket`, B:`qe4` | `li4` |
| `POST` | `sit/checkout-pca/cart-api/v1/cart-api/v2/cart/list/{countryCode}` | H:`Cookie`, H:`x-myra-traffic-bucket`, Q:`language`, B:`xe4` | `li4` |
| `POST` | `sit/checkout-pca/cart-api/v1/cart-api/v2/cart/{countryCode}` | H:`Cookie`, H:`x-myra-traffic-bucket`, Q:`language`, B:`qe4` | `li4` |
| `GET` | `sit/checkout-pca/cart-api/v1/cart-api/v2/cart/{customerNumber}` | H:`x-myra-traffic-bucket` | `li4` |
| `GET` | `sit/checkout-pca/cart-api/v1/cart-api/v3/cart/customer/{customerNumber}` | Q:`zoneId` | `li4` |
| `POST` | `sit/checkout-pca/cart-api/v1/cart-api/v3/cart/list/{countryCode}` | Q:`cartId`, Q:`language`, Q:`customerNumber`, Q:`ssoId`, Q:`zoneId`, B:`xe4` | `li4` |
| `DELETE` | `sit/checkout-pca/cart-api/v1/cart-api/v3/cart/{countryCode}` | Q:`cartId`, Q:`erpNumber`, Q:`language`, Q:`customerNumber`, Q:`ssoId`, Q:`zoneId` | `li4` |
| `GET` | `sit/checkout-pca/cart-api/v1/cart-api/v3/cart/{countryCode}` | Q:`cartId`, Q:`language`, Q:`customerNumber`, Q:`ssoId`, Q:`isMergeEnabled`, Q:`zoneId` | `li4` |
| `PATCH` | `sit/checkout-pca/cart-api/v1/cart-api/v3/cart/{countryCode}` | Q:`cartId`, Q:`language`, Q:`customerNumber`, Q:`ssoId`, Q:`zoneId`, B:`qe4` | `li4` |
| `POST` | `sit/checkout-pca/cart-api/v1/cart-api/v3/cart/{countryCode}` | Q:`cartId`, Q:`language`, Q:`customerNumber`, Q:`ssoId`, Q:`zoneId`, B:`qe4` | `li4` |
| `GET` | `sit/vlt/edd-api/v1/my-api/edd/v1` | Q:`country`, Q:`articleNumber`, Q:`zipCode`, Q:`languageid`, Q:`zone` | `fna` |
| `GET` | `suggest?version=2.0.0` | Q:`RegistrationDbStorage.Columns.LOCALE`, Q:`q`, Q:`assortment`, H:`x-myra-traffic-bucket` | `kki` |

### emobilitySDK_release
Basis: `https://emobility.lidl.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `/api/v1/country/{country}` |  | `mt9<gt6>` |
| `GET` | `/api/v1/{country}/address` |  | `mt9<rh2>` |
| `PUT` | `/api/v1/{country}/address/{addressId}` | B:`rdw` | `mt9<(leer)>` |
| `PATCH` | `/api/v1/{country}/coupon/{userPromotionId}/activate` |  | `mt9<(leer)>` |
| `PATCH` | `/api/v1/{country}/coupon/{userPromotionId}/deactivate` |  | `mt9<(leer)>` |
| `POST` | `/api/v1/{country}/form` | B:`dxo` | `mt9<(leer)>` |
| `GET` | `/api/v1/{country}/invoice/{transactionId}/pdf` |  | `mt9<cx4>` |
| `POST` | `/api/v1/{country}/preauth/request` | B:`u7m` | `mt9<j7m>` |
| `GET` | `/api/v1/{country}/preauth/session` | Q:`chargePointType` | `mt9<v7m>` |
| `PATCH` | `/api/v1/{country}/preauth/status` | B:`fhw` | `mt9<(leer)>` |
| `GET` | `/api/v1/{country}/user` |  | `mt9<eqw>` |
| `GET` | `/api/v1/{country}/user/contract/{connectorId}` | Q:`promotionId` | `mt9<hm6>` |
| `DELETE` | `/api/v1/{country}/user/favorite/{chargePointId}` |  | `mt9<List<vua>>` |
| `POST` | `/api/v1/{country}/user/favorite/{chargePointId}` |  | `mt9<List<vua>>` |
| `GET` | `/api/v2/{country}/coupons` | Q:`chargePointType` | `mt9<uf7>` |
| `POST` | `/api/v3/{country}/pending-charges` |  | `mt9<mel>` |
| `GET` | `api/v1/{country}/form/{id}` |  | `mt9<oob>` |
| `PUT` | `api/v1/{country}/pending-charge/{transactionId}` |  | `mt9<lel>` |
| `GET` | `api/v2/{country}/charge-log/{transactionId}` |  | `mt9<dx4>` |
| `GET` | `api/v2/{country}/cp/connector/{evseId}` |  | `mt9<qa6>` |
| `GET` | `api/v2/{country}/cp/{id}` |  | `mt9<ix4>` |
| `GET` | `api/v2/{country}/cps` |  | `mt9<lx4>` |
| `PUT` | `api/v2/{country}/user/contact` | B:`wdw` | `mt9<(leer)>` |
| `POST` | `api/v3/{country}/remote-start` | B:`xuo` | `mt9<wuo>` |
| `POST` | `api/v3/{country}/user/acceptance` | B:`d7m` | `mt9<(leer)>` |
| `GET` | `api/v4/{country}/charge-logs` |  | `mt9<fx4>` |
| `POST` | `api/v4/{country}/remote-stop` | B:`yuo` | `mt9<(leer)>` |

### employee-benefits
Basis: `https://employeeprogram.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `/bff-api/v3/{countryCode}/loyaltytab` | H:`Authorization`, H:`Accept` | `ResponseBody (raw)` |

### flashsales
Basis: `https://flashsales.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{countryId}/all` | H:`Accept-Language` | `List<FlashSaleProductResponse>` |
| `POST` | `v1/{countryId}/createOrder` | H:`Accept-Language`, B:`FlashSaleOrderInfoRequest` | `FlashSaleOrderResponse` |
| `GET` | `v1/{countryId}/getdetail/{flashSaleId}` | H:`Accept-Language` | `FlashSaleDetailResponse` |

### frederix
Basis: `(dynamisch / Health-Check)`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `.` |  | `(leer)` |

### grocerypickup
Basis: `https://grocerypickup.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/v1/orders/{orderId}/details` | H:`Accept-Language` | `hgd` |
| `POST` | `api/v1/orders/{orderId}/locker` | H:`Accept-Language` | `(leer)` |
| `POST` | `api/v1/orders/{orderId}/parking` | H:`Accept-Language`, B:`a9d` | `(leer)` |
| `GET` | `api/v1/{countryId}/stores/{storeId}/associated` | H:`Accept-Language` | `zgd` |
| `POST` | `api/v1/{countryId}/stores/{storeId}/carts/addonproducts` | H:`Accept-Language`, B:`w7d` | `gad` |
| `POST` | `api/v1/{countryId}/stores/{storeId}/carts/preauth` | H:`Accept-Language`, B:`c8d` | `rad` |
| `POST` | `api/v1/{countryId}/stores/{storeId}/carts/summary` | H:`Accept-Language`, B:`i8d` | `cbd` |
| `POST` | `api/v1/{countryId}/stores/{storeId}/carts/sync` | H:`Accept-Language`, B:`o8d` | `rbd` |
| `GET` | `api/v1/{countryId}/stores/{storeId}/config` | H:`Accept-Language` | `fhd` |
| `DELETE` | `api/v1/{countryId}/stores/{storeId}/orders` | H:`Accept-Language` | `(leer)` |
| `POST` | `api/v1/{countryId}/stores/{storeId}/orders` | H:`Accept-Language`, B:`g9d` | `tfd` |
| `PUT` | `api/v1/{countryId}/stores/{storeId}/orders` | H:`Accept-Language`, B:`u8d` | `yed` |
| `GET` | `api/v1/{countryId}/stores/{storeId}/orders/collected` | H:`Accept-Language` | `kdd` |
| `GET` | `api/v1/{countryId}/stores/{storeId}/orders/details` | H:`Accept-Language` | `ydd` |
| `GET` | `api/v1/{countryId}/stores/{storeId}/orders/status` | H:`Accept-Language` | `ded` |
| `POST` | `api/v1/{countryId}/stores/{storeId}/timeslots/availables` | H:`Accept-Language`, B:`p9d` | `whd` |
| `POST` | `api/v1/{countryId}/stores/{storeId}/timeslots/suggested` | H:`Accept-Language`, B:`v9d` | `nid` |

### home
Basis: `https://home.lidlplus.com/api/ bzw. /configuration/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/config/{zoneId}` | H:`Segment-Ids`, H:`UserLevel` | `HomeConfigResponse` |
| `POST` | `v2/{country}/home/anonymous` | H:`homeId`, H:`UserLevel`, B:`HomeBodyRequest` | `ResponseBody (raw)` |
| `POST` | `v2/{country}/home/logged` | H:`homeId`, H:`Segment-Ids`, H:`UserLevel`, B:`HomeBodyRequest` | `ResponseBody (raw)` |

### integration
Basis: `https://worldofneeds.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `app/{sectionName}/v{version}/countries/{countryCode}/worlds/{worldId}` | Q:`RegistrationDbStorage.Columns.ENC_TAGS`, H:`Segment-Ids` | `ResponseBody (raw)` |

### inviteyourfriends
Basis: `https://inviteyourfriends.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `v2/sessions/{session}/guests` | H:`Country-Code` | `(leer)` |
| `POST` | `v2/sessions/{session}/guests/validation` | H:`Country-Code` | `(leer)` |
| `POST` | `v2/{country}/sessions` |  | `SessionsCreateResponseModel` |
| `POST` | `v2/{country}/sessions/share/{entityType}/{entityId}` |  | `SessionsShareCreateResponseModel` |
| `GET` | `v2/{country}/sessions/{sessionHash}` |  | `SessionResponseModel` |

### lib_release
Basis: `https://eventtracker.dsa.apps.schwarz/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `/v4/json/ingest` | B:`wxo`, H:`SCRM-DataType`, H:`SCRM-Version` | `(leer)` |

### libs-tracking-adobe-experience
Basis: `https://eventtracker.dsa.apps.schwarz/ / https://myip.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `/v4/json/ingest` | B:`wxo`, H:`SCRM-DataType`, H:`SCRM-Version` | `(leer)` |
| `GET` | `?format=json` |  | `ugf` |

### libs-unleash
Basis: `https://unleash-mobile.scrm.apps.schwarz/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/frontend` | Q*:`Map<String, String>`, H*:`Map<String, String>` | `w8v` |
| `POST` | `api/frontend/client/metrics` | B:`dhi`, H*:`Map<String, String>` | `(leer)` |

### lidlplusPaymentsSDK
Basis: `https://eticket.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `/lidlplus/{country}/eTicket/v1/status` |  | `ETicketStatusApiModel` |
| `PUT` | `/lidlplus/{country}/eTicket/v1/status` | B:`ETicketStatusApiModel` | `(leer)` |

### lottery
Basis: `https://stampcard.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v4/{country}/user/promotions` | Q:`storeId` | `StampCardLotteryModel` |
| `PATCH` | `v4/{country}/user/promotions/{id}/cards/send` |  | `(leer)` |
| `PATCH` | `v4/{country}/user/promotions/{id}/cards/view` |  | `(leer)` |
| `GET` | `v4/{country}/user/promotions/{id}/congrats` |  | `CongratulationsModel` |
| `GET` | `v4/{country}/user/promotions/{id}/detail` |  | `DetailModel` |
| `PATCH` | `v4/{country}/user/promotions/{id}/legalterms/accept` |  | `(leer)` |
| `PATCH` | `v4/{country}/user/promotions/{id}/start` |  | `(leer)` |

### loyalty
Basis: `(Loyalty-Cards-Service, Host dynamisch)`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v2/{countryCode}/{segmentationId}` |  | `LoyaltyCardsResponse` |

### metahome
Basis: `https://home.lidlplus.com/api/ bzw. /configuration/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/config/{zoneId}` | H:`Segment-Ids`, H:`UserLevel` | `HomeConfigResponse` |
| `POST` | `v2/{country}/home/anonymous` | H:`homeId`, H:`UserLevel`, B:`HomeBodyRequest` | `ResponseBody (raw)` |
| `POST` | `v2/{country}/home/logged` | H:`homeId`, H:`Segment-Ids`, H:`UserLevel`, B:`HomeBodyRequest` | `ResponseBody (raw)` |

### offers
Basis: `https://offers.lidlplus.com/app/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v4/{countryCode}/{store}/offers` |  | `OfferListResponse` |
| `GET` | `v4/{countryCode}/{store}/offers/{id}` |  | `OfferDetailResponse` |

### opengift
Basis: `https://opengift.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `(@Url)` | U:`String` | `ResponseBody (raw)` |
| `GET` | `/users/api/v1/{country}/triggeredBoxes/me/detail` | Q:`worldId`, H:`Accept-Language` | `iz8` |
| `PATCH` | `/users/api/v7/{country}/opengift/me/{campaignId}/{boxId}/opened` | H:`Accept-Language`, H:`Segment-Ids` | `(leer)` |
| `GET` | `v6/{country}/users/{id}/opengift/current` | H:`Accept-Language`, H:`Segment-Ids` | `n8k` |
| `PATCH` | `v6/{country}/users/{id}/opengift/current/boxes/{boxId}/opened` | H:`Accept-Language`, H:`Segment-Ids` | `(leer)` |
| `GET` | `v6/{country}/users/{id}/opengift/current/detail` | H:`Accept-Language`, H:`Segment-Ids` | `lz8` |

### paymentsSDK
Basis: `https://payments.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `/api/addresses/v1` |  | `AddressListResponse` |
| `GET` | `/api/addresses/v1/{addressid}` |  | `AddressResponse` |
| `GET` | `/payment-methods/v1/{tender}/{country}/{customer}/{paymentMethodId}/subscriptions` |  | `SubscriptionsResponse` |
| `GET` | `/payment-methods/v1/{tender}/{country}/{customer}/{paymentMethodId}/transactions` |  | `TransactionsResponse` |
| `PATCH` | `/payment-methods/v2/{tender}/{country}` | B:`SetPaymentMethodRequest` | `(leer)` |
| `GET` | `/payment-methods/v2/{tender}/{country}/default-payment-method-info` |  | `DefaultPaymentMethodInfoResponse` |
| `POST` | `/payment-methods/v2/{tender}/{country}/validate-default-payment-method-info` | B:`ValidateDefaultPaymentMethodData` | `ValidateDefaultPaymentMethodInfoResponse` |
| `DELETE` | `/payment-methods/v2/{tender}/{country}/{customer}/payment-methods/{id}` |  | `(leer)` |
| `POST` | `/payment-methods/v2/{tender}/{country}/{customer}/qr` | B:`QrRequest`, H:`X-Session-Id`, H:`DeviceId`, H:`Pin-Token` | `QrResponse` |
| `GET` | `/payment-methods/v2/{tender}/{country}/{customer}/users/{sepaId}/limit` | H:`X-Session-Id`, H:`DeviceId` | `SepaPaymentLimitResponse` |
| `GET` | `/payment-methods/v3/{tender}/{country}/{customer}/all` |  | `GenericPaymentMethodsResponse` |
| `GET` | `/psp/v1/configuration/{tender}/{country}` |  | `ConfigurationResponse` |
| `POST` | `/psp/v1/{tender}/{country}/{customer}/payment-methods/top-up` | H:`DeviceId`, B:`AddBalanceRequest` | `AddBalanceResponse` |
| `POST` | `/psp/v1/{tender}/{country}/{customer}/payment-methods/{paymentId}/top-up` | H:`DeviceId`, B:`AddBalanceRequest` | `AddBalanceResponse` |
| `POST` | `/psp/v3/{tender}/{country}/{customer}/preauth` | B:`PreAuthStandardRequest`, H:`X-Session-Id`, H:`DeviceId`, H:`Pin-Token` | `PreAuthStandardResponse` |
| `POST` | `/user-profiles/v2/{tender}/{country}` | B:`CreateProfileRequest` | `(leer)` |
| `PUT` | `/user-profiles/v2/{tender}/{country}/address` | B:`AddressRequest` | `(leer)` |
| `POST` | `/user-profiles/v2/{tender}/{country}/pin` | B:`CreatePinRequest` | `(leer)` |
| `PUT` | `/user-profiles/v2/{tender}/{country}/pin` | H:`OTP-Token`, B:`ForgotPinRequest` | `(leer)` |
| `PUT` | `/user-profiles/v2/{tender}/{country}/pin` | H:`Pin-Token`, B:`ChangePinRequest` | `(leer)` |
| `POST` | `/user-profiles/v2/{tender}/{country}/pin/validate` | B:`ValidatePinRequest` | `ValidatePinResult` |
| `POST` | `/user-profiles/v2/{tender}/{country}/send-otp` |  | `(leer)` |
| `POST` | `/user-profiles/v2/{tender}/{country}/validate-otp` | B:`ValidateOTPRequest` | `ValidateOTPResultResponse` |
| `DELETE` | `/user-profiles/v2/{tender}/{country}/{customer}` |  | `(leer)` |
| `PUT` | `/user-profiles/v3/{tender}/{country}/{customer}/activate` | B:`ActivateRequest` | `ActivateResult` |
| `GET` | `/user-profiles/v6/{tender}/{country}/{customer}` |  | `PaymentProfileResponse` |
| `GET` | `psp/v1/{tender}/{country}/transaction/{transactionId}` |  | `PollingTransactionStatusResponse` |
| `POST` | `psp/v1/{tender}/{country}/{customer}/enrollment/{paymentMethodType}` | H:`X-Session-Id`, H:`deviceId` | `PaymentTypeEnrollmentResponse` |
| `GET` | `psp/v2/{tender}/{country}/transactions/last-accepted` |  | `LastAcceptedResponse` |
| `GET` | `user-profiles/v2/{tender}/{country}/check-mail-validated` |  | `IsMailVerifiedResult` |
| `POST` | `user-profiles/v2/{tender}/{country}/send-validation-email` |  | `IsMailSentResult` |

### personalisedsurveys
Basis: `https://persosurveys.lidlplus.com/client/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{country}/surveys/{surveyId}` |  | `ktt` |
| `PUT` | `v1/{country}/surveys/{surveyId}/questions/{questionId}/answer` | B:`dl0` | `(leer)` |

### productcatalog
Basis: `https://product-catalog.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/app/v1/{isoCountryCode}/store/{storeId}/categories` |  | `akm` |
| `GET` | `api/app/v1/{isoCountryCode}/store/{storeId}/categories/{categoryId}/categories` |  | `akm` |
| `GET` | `api/app/v1/{isoCountryCode}/store/{storeId}/categories/{categoryId}/categories/{subcategoryId}/products` | Q:`skip`, Q:`limit`, Q:`date` | `dkm` |
| `GET` | `api/app/v1/{isoCountryCode}/store/{storeId}/categories/{categoryId}/products` | Q:`skip`, Q:`limit`, Q:`date` | `dkm` |
| `GET` | `api/app/v1/{isoCountryCode}/store/{storeId}/products/{productId}` | Q:`date` | `cwm` |
| `GET` | `api/app/v1/{isoCountryCode}/store/{storeId}/search` | Q:`q`, Q:`date` | `som` |
| `GET` | `api/app/v1/{isoCountryCode}/store/{storeId}/startingpage` | Q:`date` | `hqm` |
| `POST` | `api/app/v1/{isoCountryCode}/useractivity` | B:`epf` | `(leer)` |

### products-featured
Basis: `https://productshowcase.lidlplus.com/featured/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{country}/info/{productId}` |  | `vim` |
| `GET` | `v2/{country}/products` | Q:`channel`, Q:`RegistrationDbStorage.Columns.ENC_TAGS` | `List<vim>` |

### products-recommended
Basis: `https://productshowcase.lidlplus.com/recommended/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{country}/{storeId}` |  | `List<tim>` |

### products-related
Basis: `https://productshowcase.lidlplus.com/related/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{country}/{productId}/{storeId}` |  | `List<uim>` |

### productshowcase
Basis: `https://productshowcase.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `carrousels/v1/dynamic/{country}/{storeId}/{moduleName}` |  | `n9n` |

### profile
Basis: `https://devices.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `PUT` | `v4/device` | B:`DeviceRequestDTO` | `(leer)` |

### profile-user
Basis: `https://profile.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/profile/salesforceid` |  | `String` |
| `POST` | `v1/updateCountryInfo` | B:`jfn` | `mfn` |
| `POST` | `v1/upsertProfile` | B:`pfn` | `sfn` |
| `GET` | `v1/{country}/loyalty` |  | `String` |

### purchaselottery
Basis: `https://purchaselottery.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `(@Url)` | U:`String` | `String` |
| `GET` | `v2/{country}/lotteries` | H:`Accept-Language`, Q:`userId` | `List<jzc>` |
| `GET` | `v2/{country}/lotteries/{id}` | H:`Accept-Language` | `wtc` |
| `PATCH` | `v2/{country}/lotteries/{id}/redeemed` | H:`Accept-Language` | `(leer)` |

### purchasesummary
Basis: `https://summary.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `DELETE` | `v3/{country}/notifications` | Q:`ticketId` | `(leer)` |
| `GET` | `v3/{country}/tickets/{id}/summary` | H:`Accept-Language`, H:`Segment-Ids` | `PurchaseSummaryAggregatorResponse` |

### push
Basis: `https://push-notifications.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `api/v2/push/device` | H:`Segment-Ids`, B:`SetDeviceRegistrationRequest` | `(leer)` |
| `DELETE` | `api/v2/push/device/{country}` | H:`Segment-Ids` | `(leer)` |

### rewards
Basis: `https://stampcard.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v3/{country}/user/promotions` | Q:`storeId` | `StampCardRewardsModel` |
| `PATCH` | `v3/{country}/user/promotions/{id}/cards` | B:`List<UUID>` | `(leer)` |
| `GET` | `v3/{country}/user/promotions/{id}/congrats` |  | `CongratulationsModel` |
| `GET` | `v3/{country}/user/promotions/{id}/detail` |  | `DetailDataModel` |
| `PATCH` | `v3/{country}/user/promotions/{id}/started` |  | `(leer)` |

### shortcut
Basis: `https://home.lidlplus.com/configuration/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/shortcuts/{zoneId}` | H:`Segment-Ids` | `List<ShortcutDTO>` |

### stores
Basis: `https://stores.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/autocomplete/places/{country}` | Q:`input`, Q:`language`, Q:`LocationDbStorage.Columns.ENC_LAT`, Q:`LocationDbStorage.Columns.ENC_LON` | `List<PlaceModel>` |
| `GET` | `v1/autocomplete/{country}` | Q:`input`, Q:`language`, Q:`LocationDbStorage.Columns.ENC_LAT`, Q:`LocationDbStorage.Columns.ENC_LON` | `List<StoreSearchModel>` |
| `GET` | `v1/users/me/favorite/{country}` |  | `FavoriteStoreModel` |
| `PUT` | `v1/users/me/favorite/{country}` | B:`FavoriteStoreModel` | `(leer)` |
| `GET` | `v3/schedule/{storeId}` | Q:`date` | `ScheduleModel` |
| `GET` | `v4/{country}` |  | `List<StoreDetailModel>` |
| `GET` | `v5/{country}/details` | H:`storesIds` | `List<StoreDetailModel>` |

### surveys
Basis: `https://surveys.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v2/{countryCode}/surveys/{campaignId}` | H:`Accept-Language`, H:`App-Version`, H:`Segment-Ids` | `ManualCampaignResponse` |
| `GET` | `v2/{country}/surveys` | H:`Accept-Language`, H:`Segment-Ids` | `CampaignResponse` |
| `PUT` | `v2/{country}/surveys/{campaignId}/complete` | H:`Accept-Language`, B:`CompleteUserCampaignRequest` | `(leer)` |
| `POST` | `v2/{country}/surveys/{campaignId}/dismiss` |  | `(leer)` |
| `POST` | `v2/{country}/surveys/{campaignId}/visualize/{source}` |  | `(leer)` |

### thirdpartybenefit
Basis: `https://partnersbenefits.lidlplus.com/app/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v1/{country}/categories` | Q:`segmentsIds`, H:`UserLevel` | `List<mzk>` |
| `GET` | `v2/{country}/campaigns` | Q:`segmentsIds`, Q:`placementId`, H:`UserLevel` | `ResponseBody (raw)` |
| `GET` | `v2/{country}/campaigns/{id}` | Q:`segmentsIds`, Q:`level`, H:`UserLevel` | `q0l` |
| `GET` | `v2/{country}/campaigns/{id}/code` | Q:`segmentsIds`, H:`UserLevel`, Q:`level` | `wzk` |

### tickets
Basis: `https://tickets.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `v2/{country}/tickets/delete` | B:`List<String>` | `(leer)` |
| `POST` | `v2/{country}/tickets/favorite` | B:`List<String>` | `(leer)` |
| `POST` | `v2/{country}/tickets/unfavorite` | B:`List<String>` | `(leer)` |
| `GET` | `v3/{country}/invoice/{id}` |  | `ResponseBody (raw)` |
| `GET` | `v3/{country}/tickets` | Q:`yearOffset` | `List<TicketListResponse>` |
| `GET` | `v3/{country}/tickets/{id}` | H:`Accept-Language` | `TicketUnifiedResponse` |

### tipcards
Basis: `https://tipcards.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `POST` | `v1/devicestatus` | B:`DeviceStatusModel`, H:`SessionId` | `(leer)` |
| `POST` | `v1/{country}/sendemailvalidation` |  | `(leer)` |
| `GET` | `v1/{country}/tipcard` | H:`IsPushEnabled`, H:`SessionId`, H:`IsOptionalUpdate` | `GetTipcardModel` |

### travel
Basis: `https://travel.lidlplus.com/api/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `v2/{countryCode}/travel` |  | `TravelListResponse` |

### uniqueaccount
Basis: `https://aboutme.lidl.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `api/personal-data/v1` |  | `PersonalData` |

### worldofneeds
Basis: `https://worldofneeds.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `(@Url)` | U:`String` | `(leer)` |
| `DELETE` | `app/userprofilemanagement/v1/countries/{countryCode}/worlds/{worldId}/profiles/{profileId}` |  | `(leer)` |
| `GET` | `app/userprofilemanagement/v1/countries/{countryCode}/worlds/{worldId}/profiles/{profileId}` |  | `dll` |
| `GET` | `app/v1/countries/{countryCode}/worlds/{worldId}/form` |  `x-form-version: v1` | `wpb` |
| `POST` | `app/v1/countries/{countryCode}/worlds/{worldId}/form/submission` | B:`List<kqb>`, Q:`profileId` `x-form-version: v1` | `(leer)` |
| `POST` | `app/v1/countries/{countryCode}/worlds/{worldId}/gift/claim` |  | `(leer)` |
| `POST` | `app/v1/countries/{countryCode}/worlds/{worldId}/raffle/participation` |  | `(leer)` |
| `POST` | `app/v1/events` | B:`alj` | `(leer)` |

### wrapped
Basis: `https://wrapped.lidlplus.com/`

| Methode | Pfad | Parameter | Antwort |
|---|---|---|---|
| `GET` | `(@Url)` | U:`String` | `ResponseBody (raw)` |
| `GET` | `/api/v1/countries/{country}/campaigns/{campaignId}/wrapped` | H:`x-origin` | `WrappedModel` |
| `POST` | `/api/v1/countries/{country}/campaigns/{campaignId}/wrapped/complete` |  | `(leer)` |
| `POST` | `/api/v1/countries/{country}/campaigns/{campaignId}/wrapped/lottery/participate` |  | `(leer)` |
| `POST` | `/api/v1/countries/{country}/campaigns/{campaignId}/wrapped/quizzes` | B:`WrappedAssignCouponBody` | `(leer)` |
| `POST` | `/api/v1/countries/{country}/campaigns/{campaignId}/wrapped/share` |  | `(leer)` |

## 5. React-Native-Module (Hermes-Bundle)

Aus `assets/bundle.jsbundle` (Hermes v96). HTTP-Methoden sind statisch nicht ohne Disassembly bestimmbar; Pfade mit `:param` sind Express-Style-Platzhalter.

### Lidl Connect (Mobilfunk) – `https://connect.lidlplus.com/app-api`

- `/v1/:countryCode/accounts`
- `/v1/:countryCode/accounts/dashboard`
- `/v1/:countryCode/accounts/subscriptions/:subscriptionId`
- `/v1/:countryCode/accounts/subscriptions/:subscriptionId/download-contract-summary`
- `/v1/:countryCode/accounts/subscriptions/:subscriptionId/security-info`
- `/v1/:countryCode/accounts/subscriptions/:subscriptionId/sim-profile`
- `/v1/:countryCode/accounts/subscriptions/:subscriptionId/sim-swap`
- `/v1/:countryCode/accounts/subscriptions/:subscriptionId/sms-preferences`
- `/v1/:countryCode/activation-code`
- `/v1/:countryCode/billing-address`
- `/v1/:countryCode/invoice/:invoiceId/download`
- `/v1/:countryCode/invoice/:subscriptionId`
- `/v1/:countryCode/offboarding`
- `/v1/:countryCode/onboarding/complete`
- `/v1/:countryCode/onboarding/enroll`
- `/v1/:countryCode/onboarding/images`
- `/v1/:countryCode/orders/:orderId/retrypayment`
- `/v1/:countryCode/orders/:orderId/status`
- `/v1/:countryCode/otp/:sessionId/validate`
- `/v1/:countryCode/otp/send`
- `/v1/:countryCode/payment-method`
- `/v1/:countryCode/payment-method/:paymentMethodId`
- `/v1/:countryCode/plans/:SubscriptionId/alias`
- `/v1/:countryCode/plans/:SubscriptionId/cancel`
- `/v1/:countryCode/plans/:SubscriptionId/cancel-portability`
- `/v1/:countryCode/plans/:SubscriptionId/reactivate`
- `/v1/:countryCode/plans/:SubscriptionId/withdrawal`
- `/v1/:countryCode/plans/activate`
- `/v1/:countryCode/portability/:portabilityId/viewed`
- `/v1/:countryCode/products`

### Mitarbeiterprogramm – `https://employeeprogram.lidlplus.com/bff-api`

- `/v1/:countryCode/employee/activate-coupon`
- `/v1/:countryCode/employee/deactivate-coupon`
- `/v1/:countryCode/events/ingest`
- `/v1/:countryCode/home`
- `/v1/:countryCode/home/user-model`
- `/v1/:countryCode/usermodel`
- `/v4/:countryCode/employee/section`
- `/v4/:countryCode/home-module`

### Family Club – `https://familyclub.lidl.com`

- `/api/translations/familyclub/v1/`
- `/api/user-login?country_code=`
- `/api/user/familyclub/v1/`
- `/api/user/familyclub/v1/child`
- `/api/user/familyclub/v1/children`
- `/api/user/familyclub/v1/pregnancy`
- `/api/user/familyclub/v1/userinfo/reactivate`
- `/api/user/familyclub/v1/userinfo/unsubscribe`

### Badges / Achievements / Store-Challenge – `https://badges.lidl.com`

- `/achievements/`
- `/achievements/:id`
- `/achievements/me/`
- `/achievements/me/unread?language=`
- `/achievements/me/visualize/`
- `/achievements/me/visualize?language=`
- `/assignreward?language=`
- `/badges/`
- `/badges/:id`
- `/badges/:id/riddle`
- `/badges/me/`
- `/badges/me/visualize/new?language=`
- `/badges/me?language=`
- `/benefits`
- `/benefits/me?language=`
- `/inputs?language=`
- `/promotions?countryCode=`
- `/settings/me?language=`
- `/startPeriod/visualize`
- `/termsAndConditions?language=`
- `/translations?language=`
- `/userStatus/me?language=`

### Rezepte – `https://recipes-core-api-stackit.recipes.lidl`

- `/api/V1/products/`
- `/api/V1/recipes/slug/`
- `/api/v1/recommendations/recipes/personalized/generic`
- `/api/v1/recommendations/recipes/personalized/generic-no-user`
- `/api/v1/translations`

### Coupid (Spiel) – `https://coupid.lidlplus.com`

- `/play/v1/game/`
- `/play/v1/game?countryCode=`

### Sonstiges

- `/address/redirect?client_id=`
- `/api/v1/`
- `/api/v1/authenticated`
- `/api/v1/mobile/profile`
- `/api/v1/mobile/version`
- `/api/v2/`
- `/api/v3/`
- `/home-integrations/api/v1/loyalty/me?country_code=`
- `/integrations/api/v1/`
- `/users/api/v1/`
- `/v1/`

## 6. Datenmodelle (JSON, Moshi)

Feldname = JSON-Key. Typen wie im Kotlin-Code (`List<X>`, `Map<K,V>`); obfuskierte Typen (z. B. `pm7`) sind nicht auflösbar. Nullability ist im Bytecode nicht zuverlässig erkennbar.

#### `defpackage.abb` (obfuskiert)
Enum: `A`, `N`, `E`, `C`, `M`

#### `defpackage.ayw` (obfuskiert)
Enum: `Q`, `A`, `C`

#### `defpackage.bk5` (obfuskiert)
Enum: `ReturnInfo`, `Fiscal`

#### `defpackage.f0v` (obfuskiert)
Enum: `C`, `C`

#### `defpackage.f3b` (obfuskiert)
Enum: `POINTS`, `CATEGORIES`, `QUICK_CATEGORY`

#### `defpackage.g8v` (obfuskiert)
Enum: `Q`, `T`, `S`

#### `defpackage.gs0` (obfuskiert)
Enum: `OK`, `N`, `N`, `N`

#### `defpackage.hp7` (obfuskiert)
Enum: `Left`, `Right`

#### `defpackage.jl0` (obfuskiert)
Enum: `N`, `S`, `N`, `C`

#### `defpackage.k99` (obfuskiert)
Enum: `S`, `O`

#### `defpackage.l8r` (obfuskiert)
Enum: `U`, `A`, `N`

#### `defpackage.l99` (obfuskiert)
Enum: `A`, `B`, `C`, `D`, `E`, `F`, `G`

#### `defpackage.ldk` (obfuskiert)
Enum: `E`, `A`, `O`, `S`, `A`, `N`

#### `defpackage.lo8` (obfuskiert)
Enum: `A`, `P`, `R`

#### `defpackage.min` (obfuskiert)
Enum: `MonetaryDiscount`, `FreeProduct`, `SpecialPrice`

#### `defpackage.mj5` (obfuskiert)
Enum: `CODE_128`, `ITF`, `QR_C`, `PDF_417`

#### `defpackage.o04` (obfuskiert)
Enum: `R`, `A`, `F`, `C`

#### `defpackage.o0v` (obfuskiert)
Enum: `NATIVE`, `HTML`, `BROKEN_HTML`, `HARD_PRINTED`, `HGA`

#### `defpackage.okw` (obfuskiert)
Enum: `U`, `S`, `M`

#### `defpackage.pbb` (obfuskiert)
Enum: `ACTIVE`, `NO_STOCK`, `EXPIRED`, `COMING_SOON`

#### `defpackage.pd.class` (obfuskiert)
Enum: `J`

#### `defpackage.psw` (obfuskiert)
Enum: `A`, `P`, `C`

#### `defpackage.qw` (obfuskiert)
Enum: `Leaflets`, `Coupons`, `CouponPlus`, `CouponPersonalized`, `Scratch`, `Roulette`, `Penalty`, `Brochures`, `Purchase`, `InviteYourFriends`, `Benefits`, `CollectingModel`, `MyDeposits`, `AskAboutMe`, `BadgesStarted`, `BadgesReached`, `Offers`, `BadgesExpire`, `BadgesNew`, `OnlineShop`, `ShoppingList`, `AboutMe`, `EmployeeBenefits`, `ClickAndCollect`, `OpenGiftSecretBoxes`, `OpenGiftDailyDeals`, `LidlConnectPortingRejected`, `LidlConnectPortingCanceled`, `LidlConnectPortingCompleted`, `LidlConnectInvoiceAdded`, `LidlConnectPrePaymentFailed`, `LidlConnectPaymentFailure`, `LidlConnectWarningBeforeSuspension`, `LidlConnectEmergencyServicesAvailability`, `LidlConnectFinalTermination`, `LidlConnectDeleteAccount`, `LidlConnectDropOffOnboarding`, `LidlConnectPreLaunch`, `LidlConnectLaunchDay`, `LidlConnectNewContractLimit`, `Unknown`

#### `defpackage.ryu` (obfuskiert)
Enum: `C`, `C`, `G`, `F`, `M`, `L`, `SMP`

#### `defpackage.s9b` (obfuskiert)
Enum: `L`, `R`

#### `defpackage.sj5` (obfuskiert)
Enum: `Bottom`, `Top`

#### `defpackage.ubb` (obfuskiert)
Enum: `A`, `N`, `E`, `C`, `M`

#### `defpackage.ul0` (obfuskiert)
Enum: `S`, `F`, `M`, `R`

#### `defpackage.v8u` (obfuskiert)
Enum: `N`, `E`, `P`, `E`, `IGIC`

#### `defpackage.vj5` (obfuskiert)
Enum: `S`, `L`

#### `defpackage.xck` (obfuskiert)
Enum: `UNKNOWN`, `MULTIPLY`, `ADDITION`

#### `defpackage.xot` (obfuskiert)
Enum: `FEATURE`, `APP`, `URL`

#### `defpackage.y04` (obfuskiert)
Enum: `I`, `U`

#### `defpackage.z04` (obfuskiert)
Enum: `P`, `A`, `A`, `CSATA`, `CSATS`, `R`, `U`

#### `defpackage.zd5` (obfuskiert)
Enum: `Ok`, `Partial`, `Out`

#### `defpackage.ze5` (obfuskiert)
Enum: `Open`, `InTransit`, `ReadyToPickup`, `Expired`

#### `es.lidlplus.commons.configuration.repositories.model.LidlPlusConfigurationAppApiDomainGeoLocation`
| JSON-Feld | Typ |
|---|---|
| `latitude` | `Double` |
| `longitude` | `Double` |

#### `es.lidlplus.commons.configuration.repositories.model.LidlPlusConfigurationAppApiDomainLanguage`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `defaultName` | `String` |
| `enDefaultName` | `String` |
| `active` | `Boolean` |
| `default` | `Boolean` |

#### `es.lidlplus.commons.configuration.repositories.model.LidlPlusConfigurationAppApiFeaturesGetCountriesV3ModelsCountryResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `defaultName` | `String` |
| `enDefaultName` | `String` |
| `active` | `Boolean` |
| `languages` | `List<LidlPlusConfigurationAppApiDomainLanguage>` |
| `minimunAge` | `Integer` |
| `defaultGeoLocation` | `LidlPlusConfigurationAppApiDomainGeoLocation` |

#### `es.lidlplus.commons.configuration.repositories.model.LidlPlusConfigurationAppApiFeaturesGetCountryConfigurationByStoreV3CountryConfigurationModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `zoneId` | `String` |
| `currency` | `String` |
| `pushApplicationId` | `String` |
| `pushToken` | `String` |
| `active` | `List<String>` |
| `bottomBar` | `List<String>` |
| `more` | `List<String>` |
| `legal` | `List<String>` |
| `mcAppEndpoint` | `String` |
| `pushMId` | `String` |
| `isRatingPopUpEnabled` | `Boolean` |
| `moreFromLidl` | `List<String>` |
| `businessModels` | `List<SuperHomeItemModel>` |
| `firebaseConfig` | `String` |
| `purchases` | `List<String>` |
| `segmentId` | `String` |

#### `es.lidlplus.commons.configuration.repositories.model.SuperHomeItemModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `type` | `xot` |
| `iconUrl` | `String` |
| `googleAppId` | `String` |
| `huaweiAppId` | `String` |
| `androidDeeplinkUrl` | `String` |

#### `es.lidlplus.feature.brochures.data.api.Flyer`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `name` | `String` |
| `endDate` | `LocalDateTime` |
| `startDate` | `LocalDateTime` |
| `offerEndDate` | `LocalDateTime` |
| `offerStartDate` | `LocalDateTime` |
| `thumbnailUrl` | `String` |
| `viewUrl` | `String` |
| `downloadUrl` | `String` |

#### `es.lidlplus.feature.brochures.data.api.FlyerCategory`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `name` | `String` |
| `flyers` | `List<Flyer>` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletRequestPostUserActivityModel`
| JSON-Feld | Typ |
|---|---|
| `deviceId` | `String` |
| `eventName` | `String` |
| `itemName` | `String` |
| `itemLocation` | `String` |
| `campaignId` | `String` |
| `clientId` | `String` |
| `itemId` | `String` |
| `itemIds` | `List<String>` |
| `itemContent` | `String` |
| `productWawiId` | `String` |
| `productWawiIds` | `List<String>` |
| `productPrice` | `BigDecimal` |
| `productCurrencySymbol` | `String` |
| `productHasDiscount` | `Boolean` |
| `productPriceType` | `String` |
| `productMainBgColor` | `String` |
| `productDiscountBgColor` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseCampaignDetailConfigModel`
| JSON-Feld | Typ |
|---|---|
| `showViewedBadge` | `boolean` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseCampaignDetailDisclaimersModel`
| JSON-Feld | Typ |
|---|---|
| `content` | `List<String>` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseCampaignDetailModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `subtitle` | `String` |
| `products` | `List<DigitalLeafletResponseProductModel>` |
| `config` | `DigitalLeafletResponseCampaignDetailConfigModel` |
| `related` | `List<DigitalLeafletResponseCampaignRelatedModel>` |
| `disclaimers` | `DigitalLeafletResponseCampaignDetailDisclaimersModel` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseCampaignGroupModel`
| JSON-Feld | Typ |
|---|---|
| `campaigns` | `List<DigitalLeafletResponseCampaignModel>` |
| `title` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseCampaignGroupsModel`
| JSON-Feld | Typ |
|---|---|
| `groups` | `List<DigitalLeafletResponseCampaignGroupModel>` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseCampaignModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `subtitle` | `String` |
| `kind` | `k99` |
| `image4x3Url` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseCampaignRelatedModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `subtitle` | `String` |
| `image4x3Url` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponsePriceModel`
| JSON-Feld | Typ |
|---|---|
| `price` | `BigDecimal` |
| `symbol` | `String` |
| `crossOutOldPrice` | `boolean` |
| `theme` | `DigitalLeafletResponsePriceThemeModel` |
| `priceType` | `DigitalLeafletResponsePriceModel.a` |
| `altPrice` | `BigDecimal` |
| `altSymbol` | `String` |
| `discount` | `String` |
| `title` | `String` |
| `oldPricePrefix` | `String` |
| `oldPrice` | `BigDecimal` |
| `altOldPrice` | `BigDecimal` |
| `disclaimers` | `List<String>` |
| `oldPriceAnnotation` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponsePriceModel.a`
Enum: `S`, `L`

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponsePriceThemeModel`
| JSON-Feld | Typ |
|---|---|
| `main` | `DigitalLeafletResponsePriceThemeSpanModel` |
| `discount` | `DigitalLeafletResponsePriceThemeSpanModel` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponsePriceThemeSpanModel`
| JSON-Feld | Typ |
|---|---|
| `backgroundColor` | `String` |
| `textColor` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailBadgeModel`
| JSON-Feld | Typ |
|---|---|
| `type` | `DigitalLeafletResponseProductDetailBadgeModel.a` |
| `title` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailBadgeModel.a`
Enum: `A`, `A`, `A`, `A`, `S`, `S`, `S`, `S`, `S`, `S`

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailConfigModel`
| JSON-Feld | Typ |
|---|---|
| `hideShare` | `boolean` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailEnergeticInformationModel`
| JSON-Feld | Typ |
|---|---|
| `withVariants` | `DigitalLeafletResponseProductDetailEnergeticInformationWithVariantsModel` |
| `withoutVariants` | `DigitalLeafletResponseProductDetailEnergeticInformationWithoutVariantsModel` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailEnergeticInformationWithVariantsModel`
| JSON-Feld | Typ |
|---|---|
| `types` | `List<? extends l99>` |
| `url` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailEnergeticInformationWithoutVariantsModel`
| JSON-Feld | Typ |
|---|---|
| `type` | `l99` |
| `scaleUrl` | `String` |
| `dataSheetUrl` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailLogoModel`
| JSON-Feld | Typ |
|---|---|
| `imageUrl` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `wawiId` | `String` |
| `storeStockId` | `String` |
| `title` | `String` |
| `subtitle` | `String` |
| `imageUrls` | `List<String>` |
| `logos` | `List<DigitalLeafletResponseProductDetailLogoModel>` |
| `mainPrice` | `DigitalLeafletResponsePriceModel` |
| `shippingInfo` | `String` |
| `brand` | `String` |
| `badges` | `List<DigitalLeafletResponseProductDetailBadgeModel>` |
| `relatedProducts` | `List<DigitalLeafletResponseProductDetailRelatedProductModel>` |
| `config` | `DigitalLeafletResponseProductDetailConfigModel` |
| `articleNumber` | `String` |
| `ecommerceId` | `String` |
| `description` | `String` |
| `online` | `Boolean` |
| `ecommerceUrl` | `String` |
| `energeticInformation` | `DigitalLeafletResponseProductDetailEnergeticInformationModel` |
| `rating` | `DigitalLeafletResponseProductDetailRatingModel` |
| `legalTexts` | `List<String>` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailRatingModel`
| JSON-Feld | Typ |
|---|---|
| `count` | `int` |
| `stars` | `BigDecimal` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductDetailRelatedProductModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `wawiId` | `String` |
| `title` | `String` |
| `imageUrl` | `String` |

#### `es.lidlplus.feature.digitalleaflet.data.api.model.DigitalLeafletResponseProductModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `wawiId` | `String` |
| `title` | `String` |
| `subtitle` | `String` |
| `brand` | `String` |
| `additionalInfo` | `String` |
| `logos` | `List<DigitalLeafletResponseProductDetailLogoModel>` |
| `mainPrice` | `DigitalLeafletResponsePriceModel` |
| `isOnline` | `boolean` |
| `isStore` | `boolean` |
| `energeticTypes` | `List<? extends l99>` |
| `badges` | `List<DigitalLeafletResponseProductDetailBadgeModel>` |
| `imageUrl` | `String` |
| `articleNumber` | `String` |

#### `alerts.data.v1.model.AlertModel`
| JSON-Feld | Typ |
|---|---|
| `alertId` | `String` |
| `alertConfigId` | `String` |
| `alertUniId` | `String` |
| `section` | `qw` |
| `title` | `String` |
| `text` | `String` |
| `date` | `OffsetDateTime` |
| `elementId` | `String` |
| `hasNewFeature` | `boolean` |
| `status` | `AlertModel.a` |
| `sharedAlertId` | `String` |

#### `alerts.data.v1.model.AlertModel.a`
Enum: `NEW`, `PENDING`, `VISITED`

#### `alerts.data.v1.model.DeleteAlertModel`
| JSON-Feld | Typ |
|---|---|
| `alertId` | `String` |

#### `alerts.data.v1.model.DeleteAllAlertsModel`
| JSON-Feld | Typ |
|---|---|
| `count` | `String` |

#### `alerts.data.v1.model.PendingAlertsModel`
| JSON-Feld | Typ |
|---|---|
| `userAlertId` | `String` |
| `sharedAlertId` | `String` |

#### `alerts.data.v1.model.PendingAlertsRequestModel`
| JSON-Feld | Typ |
|---|---|
| `alerts` | `List<PendingAlertsModel>` |

#### `alerts.data.v1.model.ReadAlertModel`
| JSON-Feld | Typ |
|---|---|
| `alertId` | `String` |

#### `alerts.data.v1.model.UnreadAlertModel`
| JSON-Feld | Typ |
|---|---|
| `count` | `Integer` |

#### `announcements.data.v1.AnnouncementModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `type` | `String` |
| `title` | `String` |
| `primaryText` | `String` |
| `secondaryText` | `String` |
| `url` | `String` |
| `notificationId` | `String` |
| `deepLink` | `String` |
| `imageUrl` | `String` |
| `acceptButtonText` | `String` |
| `storeKey` | `String` |
| `alternativeTextImage` | `String` |

#### `announcements.data.v1.AnnouncementViewedRequest`
| JSON-Feld | Typ |
|---|---|
| `notificationId` | `String` |

#### `appupdate.data.rest.swagger.lidlAppVersions.v1.model.Response`
| JSON-Feld | Typ |
|---|---|
| `code` | `gs0` |

#### `branddealsads.data.api.model.BrandDealModel`
| JSON-Feld | Typ |
|---|---|
| `type` | `BrandDealModel.a` |
| `imageUrl` | `String` |
| `adId` | `String` |
| `adTemplateId` | `String` |
| `url` | `String` |
| `promotion` | `BrandDealModel.PromotionContent` |
| `altText` | `String` |
| `adType` | `BrandDealModel.b` |
| `position` | `int` |
| `sponsoredContent` | `BrandDealModel.SponsoredContent` |

#### `branddealsads.data.api.model.BrandDealModel.PromotionContent`
| JSON-Feld | Typ |
|---|---|
| `promotionId` | `String` |
| `title` | `String` |
| `discount` | `String` |

#### `branddealsads.data.api.model.BrandDealModel.SponsoredContent`
| JSON-Feld | Typ |
|---|---|
| `advertiserName` | `String` |
| `financerName` | `String` |

#### `branddealsads.data.api.model.BrandDealModel.a`
Enum: `A`, `P`

#### `branddealsads.data.api.model.BrandDealModel.b`
Enum: `CPM`, `CPC`, `CPA`, `CPAWO`

#### `branddealsads.data.api.model.BrandDealsSessionResponse`
| JSON-Feld | Typ |
|---|---|
| `settings` | `BrandDealsSettingsResponse` |
| `visibleAds` | `List<BrandDealModel>` |

#### `branddealsads.data.api.model.BrandDealsSettingsResponse`
| JSON-Feld | Typ |
|---|---|
| `format` | `BrandDealsSettingsResponse.a` |
| `autoscroll` | `BrandDealsSettingsResponse.AutoScrollSettingsResponse` |

#### `branddealsads.data.api.model.BrandDealsSettingsResponse.AutoScrollSettingsResponse`
| JSON-Feld | Typ |
|---|---|
| `enabled` | `boolean` |
| `timeIntervalMs` | `int` |

#### `branddealsads.data.api.model.BrandDealsSettingsResponse.a`
Enum: `LEGACY`, `IAB_100`, `IAB_150`

#### `branddealsads.data.api.model.ClaimEventBody`
| JSON-Feld | Typ |
|---|---|
| `placementId` | `String` |
| `initialPosition` | `Integer` |
| `triggerPosition` | `Integer` |

#### `branddealsads.data.api.model.CouponCard`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `image` | `String` |
| `type` | `String` |
| `offerTitle` | `String` |
| `title` | `String` |
| `offerDescriptionShort` | `String` |
| `startValidityDate` | `Instant` |
| `endValidityDate` | `Instant` |
| `isActivated` | `boolean` |
| `promotionId` | `String` |
| `isSpecial` | `boolean` |
| `hasAsterisk` | `boolean` |
| `isHappyHour` | `boolean` |
| `tagSpecial` | `String` |
| `firstColor` | `String` |
| `firstFontColor` | `String` |
| `secondaryColor` | `String` |
| `secondaryFontColor` | `String` |

#### `branddealsads.data.api.model.DispatchEventBody`
| JSON-Feld | Typ |
|---|---|
| `adTemplateId` | `String` |
| `promotionId` | `String` |
| `placementId` | `String` |
| `adType` | `String` |
| `initialPosition` | `Integer` |
| `triggerPosition` | `Integer` |

#### `clickandpick.data.api.models.ClickandpickCampaignResponseModel`
| JSON-Feld | Typ |
|---|---|
| `areReservationsPossible` | `boolean` |

#### `clickandpick.data.api.models.ClickandpickCartAddProductRequestModel`
| JSON-Feld | Typ |
|---|---|
| `quantity` | `int` |

#### `clickandpick.data.api.models.ClickandpickCartAddProductResponseModel`
| JSON-Feld | Typ |
|---|---|
| `quantityAdded` | `int` |
| `quantityOfProductInCart` | `int` |
| `totalItems` | `int` |
| `location_table` | `List<String>` |

#### `clickandpick.data.api.models.ClickandpickCartCartResponseModel`
| JSON-Feld | Typ |
|---|---|
| `storeId` | `String` |
| `price` | `ClickandpickCartPriceModel` |
| `totalItems` | `int` |
| `productsInTheShop` | `List<ClickandpickCartProductResponseModel>` |
| `productsNotAvailable` | `List<ClickandpickCartProductResponseModel>` |
| `pickUpDate` | `ClickandpickPickUpDateModel` |

#### `clickandpick.data.api.models.ClickandpickCartCheckoutProductModel`
| JSON-Feld | Typ |
|---|---|
| `productId` | `String` |
| `quantity` | `int` |

#### `clickandpick.data.api.models.ClickandpickCartCheckoutRequestModel`
| JSON-Feld | Typ |
|---|---|
| `products` | `List<ClickandpickCartCheckoutProductModel>` |
| `totalPrice` | `BigDecimal` |

#### `clickandpick.data.api.models.ClickandpickCartPriceModel`
| JSON-Feld | Typ |
|---|---|
| `taxes` | `BigDecimal` |
| `totalWithoutTaxes` | `BigDecimal` |
| `total` | `BigDecimal` |

#### `clickandpick.data.api.models.ClickandpickCartProductResponseModel`
| JSON-Feld | Typ |
|---|---|
| `productId` | `String` |
| `title` | `String` |
| `quantity` | `int` |
| `price` | `BigDecimal` |
| `stock` | `int` |
| `maxProductsReservation` | `int` |
| `status` | `zd5` |
| `originalAmount` | `BigDecimal` |
| `infoText` | `String` |
| `brand` | `String` |

#### `clickandpick.data.api.models.ClickandpickListResponseModel`
| JSON-Feld | Typ |
|---|---|
| `products` | `List<ClickandpickSimpleProductModel>` |

#### `clickandpick.data.api.models.ClickandpickOrderResponseModel`
| JSON-Feld | Typ |
|---|---|
| `storeId` | `String` |
| `storeName` | `String` |
| `reservationNumber` | `String` |
| `creationDate` | `Instant` |
| `price` | `ClickandpickCartPriceModel` |
| `pickupDate` | `ClickandpickPickUpDateModel` |
| `status` | `ze5` |
| `daysUntilPickup` | `int` |
| `products` | `List<ClickandpickProductOfOrderResponseModel>` |

#### `clickandpick.data.api.models.ClickandpickPickUpDateModel`
| JSON-Feld | Typ |
|---|---|
| `fromTimestamp` | `int` |
| `toTimestamp` | `int` |

#### `clickandpick.data.api.models.ClickandpickPriceModel`
| JSON-Feld | Typ |
|---|---|
| `amount` | `BigDecimal` |
| `hasAsterisk` | `boolean` |
| `unitaryDescription` | `String` |
| `packaging` | `String` |
| `originalAmount` | `BigDecimal` |
| `infoText` | `String` |

#### `clickandpick.data.api.models.ClickandpickProductModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `stock` | `int` |
| `maxProductsReservation` | `int` |
| `price` | `ClickandpickPriceModel` |
| `title` | `String` |
| `imagesUrl` | `List<String>` |
| `stickers` | `List<ClickandpickStickerModel>` |
| `brand` | `String` |
| `shortDescription` | `String` |
| `longDescription` | `String` |
| `videoUrl` | `String` |

#### `clickandpick.data.api.models.ClickandpickProductOfOrderResponseModel`
| JSON-Feld | Typ |
|---|---|
| `productId` | `String` |
| `title` | `String` |
| `quantity` | `int` |
| `unitaryPrice` | `BigDecimal` |

#### `clickandpick.data.api.models.ClickandpickSimpleProductModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `description` | `String` |
| `imageUrl` | `String` |
| `stock` | `int` |
| `price` | `ClickandpickPriceModel` |
| `brand` | `String` |

#### `clickandpick.data.api.models.ClickandpickStickerModel`
| JSON-Feld | Typ |
|---|---|
| `imageUrl` | `String` |

#### `collectionmodel.campaign.detail.data.model.CampaignDetailDTO`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `imageUrl` | `String` |
| `title` | `String` |
| `subtitle` | `String` |
| `description` | `String` |
| `defaultPoints` | `int` |
| `startDate` | `Instant` |
| `endDate` | `Instant` |
| `status` | `CampaignDetailDTO.a` |
| `stores` | `List<CampaignDetailDTO.StoresDTO>` |
| `productList` | `List<CampaignDetailDTO.ProductDTO>` |
| `subType` | `CampaignDTO.CampaignDetailDTO.a` |
| `operationType` | `xck` |
| `minPurchaseValue` | `float` |
| `pointsApplied` | `BigDecimal` |

#### `collectionmodel.campaign.detail.data.model.CampaignDetailDTO.ProductDTO`
| JSON-Feld | Typ |
|---|---|
| `code` | `String` |
| `name` | `String` |

#### `collectionmodel.campaign.detail.data.model.CampaignDetailDTO.StoresDTO`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `name` | `String` |

#### `collectionmodel.campaign.detail.data.model.CampaignDetailDTO.a`
Enum: `ACTIVE`, `COMING_SOON`, `COMPLETED`

#### `collectionmodel.freepoints.data.model.CampaignDTO`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `subtitle` | `String` |
| `starts` | `Instant` |
| `ending` | `Instant` |
| `status` | `String` |
| `image` | `String` |
| `products` | `int` |
| `stores` | `int` |
| `operationType` | `xck` |
| `minPurchaseValue` | `float` |

#### `collectionmodel.freepoints.data.model.CampaignDTO.a`
Enum: `UNDEFINED`, `UNKNOWN`, `TICKET`, `PRODUCT`

#### `collectionmodel.freepoints.data.model.FinishedDTO`
| JSON-Feld | Typ |
|---|---|
| `campaigns` | `List<CampaignDTO>` |
| `internalRewards` | `List<InternalRewardDTO>` |

#### `collectionmodel.freepoints.data.model.FreePointsDTO`
| JSON-Feld | Typ |
|---|---|
| `campaigns` | `List<CampaignDTO>` |
| `internalRewards` | `List<InternalRewardDTO>` |
| `finished` | `FinishedDTO` |

#### `collectionmodel.freepoints.data.model.InternalRewardDTO`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `description` | `String` |
| `points` | `int` |
| `status` | `String` |
| `type` | `String` |
| `isBlocked` | `boolean` |

#### `collectionmodel.marketplace.data.UserPoints`
| JSON-Feld | Typ |
|---|---|
| `availablePoints` | `int` |
| `upcomingPoints` | `int` |

#### `collectionmodel.marketplace.data.dto.FiltersDTOInterface`
| JSON-Feld | Typ |
|---|---|
| `id` | `f3b` |

#### `collectionmodel.marketplace.data.dto.MarketPlaceDTO`
| JSON-Feld | Typ |
|---|---|
| `sortByControls` | `List<SortByDTO>` |
| `items` | `List<RewardDTO>` |
| `total` | `int` |
| `filterControls` | `List<? extends FiltersDTOInterface>` |
| `availablePoints` | `int` |
| `marketplaceBannerIndex` | `Integer` |
| `pointsToExpire` | `int` |
| `nextExpirationDate` | `Instant` |

#### `collectionmodel.marketplace.data.dto.RewardDTO`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `points` | `int` |
| `type` | `String` |
| `subType` | `RewardDTO.a` |
| `summary` | `String` |
| `imageUrl` | `String` |
| `state` | `RewardDTO.b` |
| `isBlocked` | `boolean` |
| `isExchangedPreviously` | `boolean` |
| `isFavorite` | `boolean` |
| `isDisabled` | `boolean` |
| `availablePromotions` | `int` |
| `exchangeButtonIsEnabled` | `boolean` |
| `availableOn` | `Instant` |
| `discountValue` | `double` |
| `discountTitle` | `String` |
| `daysUntilExpiration` | `int` |
| `relatedOnlineArticleNumber` | `String` |
| `price` | `Float` |
| `level` | `int` |

#### `collectionmodel.marketplace.data.dto.RewardDTO.a`
Enum: `FREE`, `DISCOUNT`, `MONETARY_VOUCHER`, `DISCOUNT_ONLINE_SHOP`, `MONETARY_VOUCHER_ONLINE_SHOP`, `WITH_PRICE`

#### `collectionmodel.marketplace.data.dto.RewardDTO.b`
Enum: `NOT_AVAILABLE`, `AVAILABLE`, `NO_STOCK`, `REWARD_EXCHANGED`, `COUPON_REDEEMED`, `INSUFFICIENT_POINTS`, `BLOCKED_BY_LEVEL`

#### `collectionmodel.marketplace.data.dto.SortByDTO`
| JSON-Feld | Typ |
|---|---|
| `id` | `int` |
| `translationKey` | `String` |
| `isEnabled` | `boolean` |
| `isSelected` | `boolean` |

#### `collectionmodel.marketplace.data.dto.SummaryDTO`
| JSON-Feld | Typ |
|---|---|
| `expired` | `int` |
| `total` | `int` |
| `upcoming` | `int` |
| `ratio` | `int` |
| `campaigns` | `List<SummaryDTO.CampaignDTO>` |

#### `collectionmodel.marketplace.data.dto.SummaryDTO.CampaignDTO`
| JSON-Feld | Typ |
|---|---|
| `campaignId` | `String` |
| `startDate` | `Instant` |

#### `collectionmodel.onboarding.data.model.OnBoardingDTO`
| JSON-Feld | Typ |
|---|---|
| `hasCompletedOnboarding` | `boolean` |
| `pointsToBeAdded` | `int` |

#### `collectionmodel.onboarding.data.model.OnboardingCompletedDTO`
| JSON-Feld | Typ |
|---|---|
| `pointsAdded` | `int` |

#### `collectionmodel.rewarddetail.data.model.ProductCodeDTO`
| JSON-Feld | Typ |
|---|---|
| `articleNumber` | `String` |
| `description` | `String` |

#### `collectionmodel.rewarddetail.data.model.RewardDetailDTO`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `imageUrl` | `String` |
| `summary` | `String` |
| `description` | `String` |
| `state` | `RewardDTO.b` |
| `type` | `String` |
| `subType` | `RewardDTO.a` |
| `points` | `int` |
| `availablePoints` | `int` |
| `brand` | `String` |
| `discountValue` | `double` |
| `expirationRewardDate` | `Instant` |
| `daysUntilExpiration` | `Integer` |
| `productCode` | `List<ProductCodeDTO>` |
| `legalTerms` | `String` |
| `isBlocked` | `boolean` |
| `isFavorite` | `boolean` |
| `availablePromotions` | `int` |
| `exchangeButtonIsEnabled` | `boolean` |
| `availableOn` | `Instant` |
| `discountTitle` | `String` |
| `minimumTotalPurchaseExpense` | `Double` |
| `price` | `Float` |
| `level` | `int` |

#### `collectionmodel.undo.data.UndoRewardBody`
| JSON-Feld | Typ |
|---|---|
| `userPromotionId` | `String` |

#### `collectionmodel.undo.data.UndoRewardDataDTO`
| JSON-Feld | Typ |
|---|---|
| `expiredPoints` | `int` |
| `pointsToReturn` | `int` |
| `userPromotionId` | `String` |

#### `consent.data.network.api.models.ConsentBodyRequest`
| JSON-Feld | Typ |
|---|---|
| `consents` | `List<ConsentBodyRequest.Consent>` |
| `itemName` | `String` |
| `platform` | `String` |
| `version` | `String` |
| `deviceId` | `String` |
| `tCString` | `String` |
| `oneTrustId` | `String` |
| `utiqMarTechPassId` | `String` |

#### `consent.data.network.api.models.ConsentBodyRequest.Consent`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `granted` | `Boolean` |

#### `couponplus.data.api.CouponPlusApiModel`
| JSON-Feld | Typ |
|---|---|
| `promotionId` | `String` |
| `promotionCode` | `String` |
| `type` | `CouponPlusApiModel.a` |
| `endDate` | `Instant` |
| `clusters` | `List<CouponPlusApiModel.Cluster>` |

#### `couponplus.data.api.CouponPlusApiModel.Branding`
| JSON-Feld | Typ |
|---|---|
| `backgroundColor` | `String` |
| `amountTextColor` | `String` |
| `iconUrl` | `String` |

#### `couponplus.data.api.CouponPlusApiModel.Category`
| JSON-Feld | Typ |
|---|---|
| `label` | `String` |
| `iconUrl` | `String` |
| `badgeColor` | `CouponPlusApiModel.a` |

#### `couponplus.data.api.CouponPlusApiModel.Cluster`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `type` | `CouponPlusApiModel.b` |
| `order` | `int` |
| `status` | `CouponPlusApiModel.a` |
| `reachedAmount` | `BigDecimal` |
| `reachedPercent` | `float` |
| `configuration` | `CouponPlusApiModel.Configuration` |
| `goals` | `List<CouponPlusApiModel.Goal>` |
| `intro` | `CouponPlusApiModel.Intro` |
| `initialMessage` | `CouponPlusApiModel.InitialMessage` |

#### `couponplus.data.api.CouponPlusApiModel.Configuration`
| JSON-Feld | Typ |
|---|---|
| `sectionTitle` | `String` |
| `moreInfoUrl` | `String` |
| `detailInformation` | `CouponPlusApiModel.DetailInformation` |
| `partner` | `CouponPlusApiModel.Partner` |
| `branding` | `CouponPlusApiModel.Branding` |
| `showClusterChange` | `boolean` |
| `category` | `CouponPlusApiModel.Category` |

#### `couponplus.data.api.CouponPlusApiModel.Coupon`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `userCouponId` | `String` |
| `title` | `String` |
| `discountTitle` | `String` |

#### `couponplus.data.api.CouponPlusApiModel.DetailInformation`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |

#### `couponplus.data.api.CouponPlusApiModel.Discount`
| JSON-Feld | Typ |
|---|---|
| `amount` | `BigDecimal` |

#### `couponplus.data.api.CouponPlusApiModel.Goal`
| JSON-Feld | Typ |
|---|---|
| `status` | `CouponPlusApiModel.a` |
| `value` | `BigDecimal` |
| `prize` | `CouponPlusApiModel.Prize` |

#### `couponplus.data.api.CouponPlusApiModel.InitialMessage`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |
| `imageUrl` | `String` |
| `ctaText` | `String` |
| `altTextImage` | `String` |

#### `couponplus.data.api.CouponPlusApiModel.Intro`
| JSON-Feld | Typ |
|---|---|
| `button` | `String` |
| `title` | `String` |
| `description` | `String` |
| `imageUrl` | `String` |
| `altTextImage` | `String` |

#### `couponplus.data.api.CouponPlusApiModel.Partner`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `backgroundColor` | `String` |
| `amountTextColor` | `String` |
| `goalIconUrl` | `String` |

#### `couponplus.data.api.CouponPlusApiModel.Prize`
| JSON-Feld | Typ |
|---|---|
| `type` | `CouponPlusApiModel.a` |
| `coupon` | `CouponPlusApiModel.Coupon` |
| `subscription` | `CouponPlusApiModel.Subscription` |
| `discount` | `CouponPlusApiModel.Discount` |

#### `couponplus.data.api.CouponPlusApiModel.Subscription`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `parentId` | `String` |

#### `couponplus.data.api.CouponPlusApiModel.a`
Enum: `S`, `C`, `C`

#### `couponplus.data.api.CouponPlusApiModel.b`
Enum: `S`, `C`, `C`

#### `coupons.data.api.coupons.model.ActivePromotionsCount`
| JSON-Feld | Typ |
|---|---|
| `activeCount` | `int` |

#### `coupons.data.api.coupons.model.ArticleSelection`
| JSON-Feld | Typ |
|---|---|
| `articleSelection` | `List<PromotionArticleSelected>` |

#### `coupons.data.api.coupons.model.HappyHourValidityModel`
| JSON-Feld | Typ |
|---|---|
| `fromHour` | `String` |
| `toHour` | `String` |

#### `coupons.data.api.coupons.model.MinimumConditionModel`
| JSON-Feld | Typ |
|---|---|
| `value` | `String` |
| `type` | `String` |

#### `coupons.data.api.coupons.model.PromotionArticleModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `long` |
| `description` | `String` |
| `units` | `String` |
| `image` | `String` |
| `brand` | `String` |
| `channel` | `String` |

#### `coupons.data.api.coupons.model.PromotionArticleSelected`
| JSON-Feld | Typ |
|---|---|
| `groupId` | `String` |
| `articleId` | `String` |

#### `coupons.data.api.coupons.model.PromotionAvailabilityModel`
| JSON-Feld | Typ |
|---|---|
| `apologizeStatus` | `boolean` |
| `title` | `String` |
| `text` | `String` |

#### `coupons.data.api.coupons.model.PromotionCardModel`
| JSON-Feld | Typ |
|---|---|
| `prices` | `PromotionOfferModel` |
| `levels` | `PromotionLevelsModel` |

#### `coupons.data.api.coupons.model.PromotionCharacteristicsModel`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |

#### `coupons.data.api.coupons.model.PromotionConditionsModel`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |

#### `coupons.data.api.coupons.model.PromotionDetailModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `promotionId` | `String` |
| `images` | `List<PromotionImageModel>` |
| `type` | `String` |
| `crossSelling` | `String` |
| `discount` | `PromotionDiscountModel` |
| `title` | `String` |
| `description` | `String` |
| `validity` | `PromotionValidityModel` |
| `isSpecial` | `boolean` |
| `isActivated` | `boolean` |
| `isProcessing` | `boolean` |
| `availability` | `PromotionAvailabilityModel` |
| `isRedeemed` | `boolean` |
| `isHappyHour` | `boolean` |
| `isSegmented` | `boolean` |
| `stores` | `List<String>` |
| `groups` | `List<PromotionGroupModel>` |
| `brand` | `String` |
| `characteristics` | `PromotionCharacteristicsModel` |
| `conditions` | `PromotionConditionsModel` |
| `specialPromotion` | `PromotionSpecialModel` |
| `prices` | `PromotionOfferModel` |
| `articles` | `List<PromotionArticleModel>` |
| `articlesDiscounted` | `List<PromotionArticleModel>` |
| `channel` | `String` |
| `channels` | `List<String>` |
| `navigationURL` | `String` |
| `levels` | `PromotionLevelsModel` |
| `skin` | `String` |

#### `coupons.data.api.coupons.model.PromotionDiscountModel`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |
| `hasAsterisk` | `boolean` |
| `scope` | `String` |
| `purchaseType` | `String` |
| `posType` | `String` |

#### `coupons.data.api.coupons.model.PromotionGroupArticle`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `image` | `PromotionImageModel` |
| `selected` | `boolean` |

#### `coupons.data.api.coupons.model.PromotionGroupModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `articles` | `List<PromotionGroupArticle>` |
| `title` | `String` |

#### `coupons.data.api.coupons.model.PromotionImageModel`
| JSON-Feld | Typ |
|---|---|
| `url` | `String` |
| `altText` | `String` |

#### `coupons.data.api.coupons.model.PromotionLevelsModel`
| JSON-Feld | Typ |
|---|---|
| `level` | `int` |
| `isLocked` | `boolean` |

#### `coupons.data.api.coupons.model.PromotionListModel`
| JSON-Feld | Typ |
|---|---|
| `sections` | `List<PromotionListSectionModel>` |

#### `coupons.data.api.coupons.model.PromotionListSectionModel`
| JSON-Feld | Typ |
|---|---|
| `name` | `String` |
| `promotions` | `List<PromotionModel>` |

#### `coupons.data.api.coupons.model.PromotionModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `image` | `PromotionImageModel` |
| `type` | `String` |
| `discount` | `PromotionDiscountModel` |
| `title` | `String` |
| `validity` | `PromotionValidityModel` |
| `isActivated` | `boolean` |
| `isProcessing` | `boolean` |
| `availability` | `PromotionAvailabilityModel` |
| `promotionId` | `String` |
| `isHappyHour` | `boolean` |
| `isSpecial` | `boolean` |
| `channel` | `String` |
| `channels` | `List<String>` |
| `stores` | `List<String>` |
| `groups` | `List<PromotionGroupModel>` |
| `specialPromotion` | `PromotionSpecialModel` |
| `prices` | `PromotionOfferModel` |
| `navigationURL` | `String` |
| `isTest` | `boolean` |
| `articleIds` | `List<String>` |
| `brand` | `String` |
| `levels` | `PromotionLevelsModel` |
| `skin` | `String` |

#### `coupons.data.api.coupons.model.PromotionOfferModel`
| JSON-Feld | Typ |
|---|---|
| `type` | `min` |
| `originalPrice` | `String` |
| `promotionPrice` | `String` |
| `basePrice` | `String` |
| `lowestPrice` | `String` |
| `packaging` | `String` |

#### `coupons.data.api.coupons.model.PromotionSpecialModel`
| JSON-Feld | Typ |
|---|---|
| `ConstraintLayout` | `String` |
| `color` | `String` |
| `fontColor` | `String` |

#### `coupons.data.api.coupons.model.PromotionTitleModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `?` |
| `title` | `?` |

#### `coupons.data.api.coupons.model.PromotionValidityModel`
| JSON-Feld | Typ |
|---|---|
| `start` | `OffsetDateTime` |
| `end` | `OffsetDateTime` |

#### `coupons.data.api.coupons.model.PromotionsByArticleResponseModel`
| JSON-Feld | Typ |
|---|---|
| `promotions` | `List<ResponsePromotionByArticleModel>` |

#### `coupons.data.api.coupons.model.ResponsePromotionByArticleModel`
| JSON-Feld | Typ |
|---|---|
| `articlesIds` | `List<String>` |
| `categoriesIds` | `List<String>` |
| `expiresInDays` | `int` |
| `happyHourValidity` | `HappyHourValidityModel` |
| `hasAsterisk` | `boolean` |
| `id` | `String` |
| `isHappyHour` | `boolean` |
| `isMultiArticle` | `boolean` |
| `minimumConditions` | `List<MinimumConditionModel>` |
| `promotionId` | `String` |
| `redemptionChannels` | `List<String>` |
| `status` | `String` |
| `texts` | `TextsModel` |
| `validity` | `ValidityModel` |
| `isTest` | `boolean` |
| `level` | `Integer` |
| `combinable` | `boolean` |

#### `coupons.data.api.coupons.model.TextsModel`
| JSON-Feld | Typ |
|---|---|
| `discountTitle` | `String` |
| `termsAndCondition` | `String` |
| `title` | `String` |

#### `coupons.data.api.coupons.model.ValidityModel`
| JSON-Feld | Typ |
|---|---|
| `start` | `OffsetDateTime` |
| `end` | `OffsetDateTime` |

#### `coupons.data.api.events.model.PromotionEventModel`
| JSON-Feld | Typ |
|---|---|
| `actionLocation` | `?` |
| `endValidityDate` | `?` |
| `userPromotionId` | `?` |
| `redemptionChannel` | `?` |
| `elementLevel` | `?` |
| `skin` | `?` |

#### `deposits.data.api.model.DepositDetailItemResponse`
| JSON-Feld | Typ |
|---|---|
| `usageType` | `okw` |
| `amount` | `BigDecimal` |
| `totalAmount` | `BigDecimal` |
| `count` | `int` |

#### `deposits.data.api.model.DepositDetailRedemptionResponse`
| JSON-Feld | Typ |
|---|---|
| `date` | `OffsetDateTime` |
| `store` | `StoreResponse` |

#### `deposits.data.api.model.DepositDetailResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `store` | `StoreResponse` |
| `items` | `List<DepositDetailItemResponse>` |
| `depositDate` | `OffsetDateTime` |
| `redemption` | `DepositDetailRedemptionResponse` |

#### `deposits.data.api.model.DepositItemResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `status` | `lo8` |
| `barcode` | `String` |
| `amount` | `BigDecimal` |
| `depositStore` | `StoreResponse` |
| `depositDate` | `OffsetDateTime` |
| `itemsCount` | `int` |
| `redeemedDate` | `OffsetDateTime` |
| `redeemedStore` | `StoreResponse` |

#### `deposits.data.api.model.DepositSummaryResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `amount` | `BigDecimal` |
| `store` | `StoreResponse` |
| `depositDate` | `OffsetDateTime` |
| `itemsCount` | `int` |

#### `deposits.data.api.model.DepositsResponse`
| JSON-Feld | Typ |
|---|---|
| `availableAmount` | `BigDecimal` |
| `pendingAmount` | `BigDecimal` |
| `isAutomaticRedemption` | `boolean` |
| `deposits` | `List<DepositItemResponse>` |
| `qrInfo` | `QRInfoResponse` |

#### `deposits.data.api.model.QRInfoResponse`
| JSON-Feld | Typ |
|---|---|
| `prefix` | `String` |
| `barcodeLength` | `int` |
| `totalBarcodes` | `int` |
| `separator` | `String` |
| `fillCharacter` | `String` |

#### `deposits.data.api.model.RVMRequest`
| JSON-Feld | Typ |
|---|---|
| `qrCode` | `String` |

#### `deposits.data.api.model.SettingsRequest`
| JSON-Feld | Typ |
|---|---|
| `isAutomaticRedemption` | `boolean` |

#### `deposits.data.api.model.StoreResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `name` | `String` |

#### `flashsales.data.models.FlashSaleDetailEnergyInfo`
| JSON-Feld | Typ |
|---|---|
| `iconUrl` | `String` |
| `labelUrl` | `String` |
| `dataSheetUrl` | `String` |

#### `flashsales.data.models.FlashSaleDetailPrice`
| JSON-Feld | Typ |
|---|---|
| `discountAmount` | `BigDecimal` |
| `discountPercentage` | `BigDecimal` |
| `originalAmount` | `BigDecimal` |

#### `flashsales.data.models.FlashSaleDetailPriceRule`
| JSON-Feld | Typ |
|---|---|
| `discountAmount` | `BigDecimal` |
| `quantity` | `int` |

#### `flashsales.data.models.FlashSaleDetailResponse`
| JSON-Feld | Typ |
|---|---|
| `brand` | `String` |
| `priceFormat` | `FlashSalePriceFormat` |
| `description` | `String` |
| `endValidityDate` | `Instant` |
| `id` | `String` |
| `imageUrls` | `List<String>` |
| `moreSpecs` | `String` |
| `price` | `FlashSaleDetailPrice` |
| `priceRules` | `List<FlashSaleDetailPriceRule>` |
| `status` | `abb` |
| `unitsSold` | `int` |
| `title` | `String` |
| `totalStock` | `int` |
| `energyInfo` | `FlashSaleDetailEnergyInfo` |

#### `flashsales.data.models.FlashSaleEnergyInfo`
| JSON-Feld | Typ |
|---|---|
| `iconUrl` | `String` |
| `labelUrl` | `String` |

#### `flashsales.data.models.FlashSaleListPrice`
| JSON-Feld | Typ |
|---|---|
| `originalAmount` | `BigDecimal` |
| `discountAmount` | `BigDecimal` |
| `discountPercentage` | `BigDecimal` |

#### `flashsales.data.models.FlashSaleOrderInfoRequest`
| JSON-Feld | Typ |
|---|---|
| `flashSaleId` | `String` |
| `quantity` | `int` |
| `salesChannel` | `String` |

#### `flashsales.data.models.FlashSaleOrderResponse`
| JSON-Feld | Typ |
|---|---|
| `checkoutUrl` | `String` |
| `status` | `ubb` |
| `ssoPlatformId` | `String` |

#### `flashsales.data.models.FlashSalePriceFormat`
| JSON-Feld | Typ |
|---|---|
| `currencySeparator` | `String` |
| `groupingSeparator` | `String` |
| `minDecimalDigits` | `int` |
| `maxDecimalDigits` | `int` |
| `currencyPosition` | `s9b` |
| `currency` | `String` |
| `decimalDelimiter` | `String` |

#### `flashsales.data.models.FlashSaleProductResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `title` | `String` |
| `imageUrl` | `String` |
| `endValidityDate` | `Instant` |
| `startDate` | `Instant` |
| `price` | `FlashSaleListPrice` |
| `priceDelimiter` | `String` |
| `currency` | `String` |
| `status` | `pbb` |
| `energyInfo` | `FlashSaleEnergyInfo` |

#### `home.data.network.models.HomeBodyRequest`
| JSON-Feld | Typ |
|---|---|
| `storeId` | `String` |
| `modules` | `List<HomeBodyRequest.Module>` |

#### `home.data.network.models.HomeBodyRequest.Module`
| JSON-Feld | Typ |
|---|---|
| `moduleName` | `String` |
| `aggregateVersion` | `int` |

#### `home.data.network.models.configuration.Configuration`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `modules` | `List<String>` |

#### `home.data.network.models.configuration.HomeConfigResponse`
| JSON-Feld | Typ |
|---|---|
| `configurations` | `List<Configuration>` |

#### `inviteyourfriends.data.model.SessionResponseModel`
| JSON-Feld | Typ |
|---|---|
| `sessionHash` | `String` |
| `country` | `String` |
| `entityType` | `String` |
| `entityId` | `String` |
| `entityStatus` | `l8r` |
| `campaignType` | `y04` |

#### `loyalty.data.network.api.models.LoyaltyCardsResponse`
| JSON-Feld | Typ |
|---|---|
| `activated` | `List<String>` |

#### `metahome.data.network.models.HomeBodyRequest`
| JSON-Feld | Typ |
|---|---|
| `storeId` | `String` |
| `modules` | `List<HomeBodyRequest.Module>` |

#### `metahome.data.network.models.HomeBodyRequest.Module`
| JSON-Feld | Typ |
|---|---|
| `moduleName` | `String` |
| `aggregateVersion` | `int` |

#### `metahome.data.network.models.configuration.Configuration`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `modules` | `List<String>` |

#### `metahome.data.network.models.configuration.HomeConfigResponse`
| JSON-Feld | Typ |
|---|---|
| `configurations` | `List<Configuration>` |

#### `offers.data.api.model.OfferDetailResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `offerType` | `OfferTypes` |
| `redemptionChannel` | `RedemptionChannels` |
| `category` | `OffersCategory` |
| `images` | `List<OfferImageResponse>` |
| `priceBox` | `OfferPriceBoxResponse` |
| `title` | `String` |
| `productCodes` | `OfferProductResponse` |
| `startValidityDate` | `OffsetDateTime` |
| `endValidityDate` | `OffsetDateTime` |
| `startValidityDateUTC` | `OffsetDateTime` |
| `endValidityDateUTC` | `OffsetDateTime` |
| `isFreeShipping` | `boolean` |
| `brand` | `String` |
| `description` | `String` |
| `characteristicsTitle` | `String` |
| `characteristicsDescription` | `String` |
| `termsAndConditionsTitle` | `String` |
| `termsAndConditionsDescription` | `String` |
| `packaging` | `String` |
| `pricePerUnit` | `String` |
| `lowestPrice` | `BigDecimal` |
| `featured` | `OfferFeaturedResponse` |
| `navigationUrl` | `String` |

#### `offers.data.api.model.OfferFeaturedResponse`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `backgroundColor` | `String` |
| `fontColor` | `String` |

#### `offers.data.api.model.OfferImageResponse`
| JSON-Feld | Typ |
|---|---|
| `url` | `String` |
| `altText` | `String` |

#### `offers.data.api.model.OfferItemListResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `offerType` | `OfferTypes` |
| `redemptionChannel` | `RedemptionChannels` |
| `category` | `OffersCategory` |
| `imageUrl` | `String` |
| `imageAltText` | `String` |
| `priceBox` | `OfferPriceBoxResponse` |
| `title` | `String` |
| `startValidityDate` | `OffsetDateTime` |
| `endValidityDate` | `OffsetDateTime` |
| `startValidityDateUTC` | `OffsetDateTime` |
| `endValidityDateUTC` | `OffsetDateTime` |
| `brand` | `String` |
| `packaging` | `String` |
| `pricePerUnit` | `String` |
| `featured` | `OfferFeaturedResponse` |
| `productIds` | `List<String>` |

#### `offers.data.api.model.OfferListResponse`
| JSON-Feld | Typ |
|---|---|
| `totalOffers` | `BigDecimal` |
| `offers` | `List<OfferItemListResponse>` |

#### `offers.data.api.model.OfferPriceBoxResponse`
| JSON-Feld | Typ |
|---|---|
| `hasAsterisk` | `boolean` |
| `strikethrough` | `boolean` |
| `firstColor` | `String` |
| `firstFontColor` | `String` |
| `secondColor` | `String` |
| `secondFontColor` | `String` |
| `priceSymbol` | `String` |
| `discountMessage` | `String` |
| `largePartNumeric` | `BigDecimal` |
| `largePartString` | `String` |
| `smallPartNumeric` | `BigDecimal` |
| `smallPartString` | `String` |

#### `offers.data.api.model.OfferProductDetailResponse`
| JSON-Feld | Typ |
|---|---|
| `code` | `String` |
| `name` | `String` |
| `imageUrl` | `String` |
| `brand` | `String` |

#### `offers.data.api.model.OfferProductResponse`
| JSON-Feld | Typ |
|---|---|
| `mainProducts` | `List<OfferProductDetailResponse>` |
| `secondaryProducts` | `List<OfferProductDetailResponse>` |

#### `offers.data.api.model.OfferTypes`
Enum: `S`, `S`, `S`, `S`, `S`, `S`, `S`, `S`, `S`, `S`, `O`, `O`, `O`, `O`, `O`, `unknown`

#### `offers.data.api.model.OffersCategory`
Enum: `O`, `S`, `F`, `V`, `U`

#### `offers.data.api.model.RedemptionChannels`
Enum: `O`, `S`, `V`, `U`

#### `profile.device.data.api.model.DeviceRequestDTO`
| JSON-Feld | Typ |
|---|---|
| `country_code` | `String` |
| `device_id` | `String` |
| `appVersion` | `String` |
| `adjust_id` | `String` |
| `model` | `String` |
| `brand` | `String` |
| `operating_system` | `String` |
| `operating_system_version` | `String` |
| `one_trust_id` | `String` |
| `apps_flyer_id` | `String` |

#### `purchasesummary.data.api.model.PurchaseSummaryAggregatorResponse`
| JSON-Feld | Typ |
|---|---|
| `ticketId` | `String` |
| `purchaseAmountWithoutCurrency` | `String` |
| `purchaseAmount` | `BigDecimal` |
| `isDeletedTicket` | `boolean` |
| `date` | `OffsetDateTime` |
| `isHtml` | `boolean` |
| `externalProducts` | `Map<String, ? extends Object>` |
| `hasHtmlDocument` | `boolean` |
| `origin` | `PurchaseSummaryAggregatorResponse.a` |
| `purchaseSavingsWithoutCurrency` | `String` |
| `purchaseSavings` | `BigDecimal` |
| `vendor` | `VendorResponse` |

#### `purchasesummary.data.api.model.PurchaseSummaryAggregatorResponse.a`
Enum: `S`, `HGA`

#### `purchasesummary.data.api.model.VendorResponse`
| JSON-Feld | Typ |
|---|---|
| `vendorId` | `String` |
| `vendorTransactionId` | `String` |
| `vendorLogoUrl` | `String` |

#### `push.api.model.SetDeviceRegistrationRequest`
| JSON-Feld | Typ |
|---|---|
| `deviceId` | `String` |
| `pnsHandle` | `String` |
| `platform` | `int` |
| `country` | `String` |
| `languageCode` | `String` |

#### `share.data.model.SessionsCreateResponseModel`
| JSON-Feld | Typ |
|---|---|
| `url` | `String` |

#### `share.data.model.SessionsShareCreateResponseModel`
| JSON-Feld | Typ |
|---|---|
| `url` | `String` |
| `description` | `String` |

#### `shortcut.data.network.api.models.ShortcutDTO`
| JSON-Feld | Typ |
|---|---|
| `productId` | `String` |
| `icon` | `String` |
| `title` | `String` |
| `deeplink` | `String` |

#### `stampcard.benefits.data.models.CongratulationsModel`
| JSON-Feld | Typ |
|---|---|
| `cards` | `List<CongratulationsModel.Card>` |
| `legalTerms` | `String` |

#### `stampcard.benefits.data.models.CongratulationsModel.Card`
| JSON-Feld | Typ |
|---|---|
| `id` | `UUID` |
| `benefitId` | `String` |

#### `stampcard.benefits.data.models.DetailModel`
| JSON-Feld | Typ |
|---|---|
| `promotionId` | `String` |
| `endDate` | `OffsetDateTime` |
| `information` | `DetailModel.Information` |
| `prizes` | `List<DetailModel.Prize>` |
| `configuration` | `DetailModel.Configuration` |
| `userPromotion` | `DetailModel.UserPromotion` |

#### `stampcard.benefits.data.models.DetailModel.Benefit`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `completedDate` | `Instant` |

#### `stampcard.benefits.data.models.DetailModel.Configuration`
| JSON-Feld | Typ |
|---|---|
| `stampIconUrl` | `String` |
| `unitsPerPrize` | `int` |
| `stampName` | `String` |
| `maxUnitsPerPurchase` | `Integer` |
| `maxBenefitsPerUser` | `Integer` |
| `unitsAvailable` | `DetailModel.(leer)sAvailable` |

#### `stampcard.benefits.data.models.DetailModel.Information`
| JSON-Feld | Typ |
|---|---|
| `description` | `String` |
| `moreInformationUrl` | `String` |

#### `stampcard.benefits.data.models.DetailModel.Prize`
| JSON-Feld | Typ |
|---|---|
| `description` | `String` |
| `name` | `String` |
| `imageUrl` | `String` |

#### `stampcard.benefits.data.models.DetailModel.UnitsAvailable`
| JSON-Feld | Typ |
|---|---|
| `total` | `int` |
| `available` | `int` |

#### `stampcard.benefits.data.models.DetailModel.UserPromotion`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `unitsAchieved` | `int` |
| `benefits` | `List<DetailModel.Benefit>` |
| `completedCards` | `int` |

#### `stampcard.benefits.data.models.StampCardBenefitsModel`
| JSON-Feld | Typ |
|---|---|
| `promotionId` | `String` |
| `endDate` | `OffsetDateTime` |
| `status` | `StampCardBenefitsModel.a` |
| `configuration` | `StampCardBenefitsModel.ConfigurationModel` |
| `userPromotion` | `StampCardBenefitsModel.UserPromotionModel` |
| `intro` | `StampCardBenefitsModel.IntroModel` |

#### `stampcard.benefits.data.models.StampCardBenefitsModel.ConfigurationModel`
| JSON-Feld | Typ |
|---|---|
| `stampIconUrl` | `String` |
| `unitsPerPrize` | `int` |
| `unitValue` | `BigDecimal` |
| `maxUnitsPerPurchase` | `Integer` |
| `maxBenefitsPerUser` | `Integer` |
| `unitsAvailable` | `StampCardBenefitsModel.(leer)sAvailable` |

#### `stampcard.benefits.data.models.StampCardBenefitsModel.IntroModel`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |
| `imageUrl` | `String` |
| `altTextImage` | `String` |

#### `stampcard.benefits.data.models.StampCardBenefitsModel.UnitsAvailable`
| JSON-Feld | Typ |
|---|---|
| `total` | `int` |
| `available` | `int` |

#### `stampcard.benefits.data.models.StampCardBenefitsModel.UserPromotionModel`
| JSON-Feld | Typ |
|---|---|
| `unitsAchieved` | `int` |
| `completedCards` | `int` |
| `hasCards` | `StampCardBenefitsModel.a` |

#### `stampcard.benefits.data.models.StampCardBenefitsModel.a`
Enum: `NotStarted`, `Started`, `Completed`, `Ended`, `A`, `O`

#### `stampcard.lottery.data.api.v3.CongratulationsModel`
| JSON-Feld | Typ |
|---|---|
| `promotionCode` | `String` |
| `participationsToSend` | `int` |
| `hasAcceptedLegalTerms` | `boolean` |
| `legalTerms` | `String` |
| `endDate` | `OffsetDateTime` |

#### `stampcard.lottery.data.api.v3.DetailModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `promotionId` | `UUID` |
| `promotionCode` | `String` |
| `endDate` | `OffsetDateTime` |
| `information` | `DetailModel.Information` |
| `configuration` | `DetailModel.Configuration` |
| `userPromotion` | `DetailModel.UserPromotion` |
| `prizes` | `List<DetailModel.Prize>` |

#### `stampcard.lottery.data.api.v3.DetailModel.Configuration`
| JSON-Feld | Typ |
|---|---|
| `stampColor` | `String` |
| `stampIconUrl` | `String` |
| `unitsPerPrize` | `int` |
| `stampName` | `String` |

#### `stampcard.lottery.data.api.v3.DetailModel.Information`
| JSON-Feld | Typ |
|---|---|
| `description` | `String` |
| `moreInformationUrl` | `String` |

#### `stampcard.lottery.data.api.v3.DetailModel.Participation`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `isSent` | `boolean` |
| `creationDate` | `OffsetDateTime` |

#### `stampcard.lottery.data.api.v3.DetailModel.Prize`
| JSON-Feld | Typ |
|---|---|
| `units` | `int` |
| `name` | `String` |
| `imageUrl` | `String` |

#### `stampcard.lottery.data.api.v3.DetailModel.UserPromotion`
| JSON-Feld | Typ |
|---|---|
| `unitsAchieved` | `int` |
| `participations` | `List<DetailModel.Participation>` |

#### `stampcard.lottery.data.api.v3.StampCardLotteryModel`
| JSON-Feld | Typ |
|---|---|
| `promotionId` | `UUID` |
| `promotionCode` | `String` |
| `endDate` | `OffsetDateTime` |
| `status` | `StampCardLotteryModel.a` |
| `configuration` | `StampCardLotteryModel.Configuration` |
| `userPromotion` | `StampCardLotteryModel.UserPromotion` |
| `intro` | `StampCardLotteryModel.Intro` |
| `outro` | `StampCardLotteryModel.Outro` |

#### `stampcard.lottery.data.api.v3.StampCardLotteryModel.Configuration`
| JSON-Feld | Typ |
|---|---|
| `stampColor` | `String` |
| `stampIconUrl` | `String` |
| `maxUnitsPerPurchase` | `Integer` |
| `unitValue` | `BigDecimal` |
| `unitsPerPrize` | `int` |

#### `stampcard.lottery.data.api.v3.StampCardLotteryModel.Intro`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |
| `imageUrl` | `String` |
| `altTextImage` | `String` |

#### `stampcard.lottery.data.api.v3.StampCardLotteryModel.Outro`
| JSON-Feld | Typ |
|---|---|
| `description` | `String` |
| `winnersUrl` | `String` |

#### `stampcard.lottery.data.api.v3.StampCardLotteryModel.UserPromotion`
| JSON-Feld | Typ |
|---|---|
| `unitsAchieved` | `int` |
| `hasNotViewedCards` | `boolean` |
| `participationsToSend` | `int` |

#### `stampcard.lottery.data.api.v3.StampCardLotteryModel.a`
Enum: `N`, `S`, `P`, `E`

#### `stampcard.rewards.data.models.CongratulationsCardModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `UUID` |
| `userCouponId` | `UUID` |

#### `stampcard.rewards.data.models.CongratulationsModel`
| JSON-Feld | Typ |
|---|---|
| `cards` | `List<CongratulationsCardModel>` |
| `legalTerms` | `String` |

#### `stampcard.rewards.data.models.DetailDataModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `promotionId` | `String` |
| `endDate` | `OffsetDateTime` |
| `information` | `DetailDataModel.Information` |
| `prizes` | `List<DetailDataModel.Prize>` |
| `configuration` | `DetailDataModel.Configuration` |
| `userPromotion` | `DetailDataModel.UserPromotion` |

#### `stampcard.rewards.data.models.DetailDataModel.Configuration`
| JSON-Feld | Typ |
|---|---|
| `stampIconUrl` | `String` |
| `unitsPerPrize` | `int` |
| `stampName` | `String` |

#### `stampcard.rewards.data.models.DetailDataModel.Coupon`
| JSON-Feld | Typ |
|---|---|
| `couponId` | `String` |
| `isRedeemed` | `boolean` |

#### `stampcard.rewards.data.models.DetailDataModel.Information`
| JSON-Feld | Typ |
|---|---|
| `description` | `String` |
| `moreInformationUrl` | `String` |

#### `stampcard.rewards.data.models.DetailDataModel.Prize`
| JSON-Feld | Typ |
|---|---|
| `description` | `String` |
| `name` | `String` |
| `imageUrl` | `String` |

#### `stampcard.rewards.data.models.DetailDataModel.UserPromotion`
| JSON-Feld | Typ |
|---|---|
| `unitsAchieved` | `int` |
| `coupons` | `List<DetailDataModel.Coupon>` |

#### `stampcard.rewards.data.models.StampCardRewardsModel`
| JSON-Feld | Typ |
|---|---|
| `promotionId` | `String` |
| `endDate` | `OffsetDateTime` |
| `status` | `StampCardRewardsModel.a` |
| `configuration` | `StampCardRewardsModel.Configuration` |
| `userPromotion` | `StampCardRewardsModel.UserPromotion` |
| `intro` | `StampCardRewardsModel.Intro` |

#### `stampcard.rewards.data.models.StampCardRewardsModel.Configuration`
| JSON-Feld | Typ |
|---|---|
| `stampIconUrl` | `String` |
| `unitsPerPrize` | `int` |
| `unitValue` | `BigDecimal` |
| `maxUnitsPerPurchase` | `Integer` |

#### `stampcard.rewards.data.models.StampCardRewardsModel.Intro`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `description` | `String` |
| `imageUrl` | `String` |
| `altTextImage` | `String` |

#### `stampcard.rewards.data.models.StampCardRewardsModel.UserPromotion`
| JSON-Feld | Typ |
|---|---|
| `unitsAchieved` | `int` |
| `hasNotViewedCards` | `boolean` |
| `completedCards` | `int` |

#### `stampcard.rewards.data.models.StampCardRewardsModel.a`
Enum: `NotStarted`, `Started`, `Compoleted`, `Ended`

#### `stores.selector.data.models.AmenityModel`
| JSON-Feld | Typ |
|---|---|
| `imageUrl` | `String` |
| `literalKey` | `String` |

#### `stores.selector.data.models.CountryZoneModel`
| JSON-Feld | Typ |
|---|---|
| `zoneId` | `String` |
| `isPilot` | `Boolean` |

#### `stores.selector.data.models.FavoriteStoreModel`
| JSON-Feld | Typ |
|---|---|
| `country` | `String` |
| `storeKey` | `String` |

#### `stores.selector.data.models.GeoLocationModel`
| JSON-Feld | Typ |
|---|---|
| `latitude` | `double` |
| `longitude` | `double` |

#### `stores.selector.data.models.OpeningHoursModel`
| JSON-Feld | Typ |
|---|---|
| `from` | `String` |
| `to` | `String` |

#### `stores.selector.data.models.PlaceModel`
| JSON-Feld | Typ |
|---|---|
| `placeId` | `String` |
| `placeDescription` | `String` |
| `distance` | `double` |

#### `stores.selector.data.models.ScheduleModel`
| JSON-Feld | Typ |
|---|---|
| `isOpen` | `boolean` |
| `isTemporarilyClosed` | `boolean` |
| `isPermanentlyClosed` | `boolean` |
| `openingHours` | `List<OpeningHoursModel>` |
| `reopensOn` | `String` |
| `willCloseOn` | `Integer` |
| `willOpenAt` | `WillOpenAtModel` |

#### `stores.selector.data.models.StoreDetailModel`
| JSON-Feld | Typ |
|---|---|
| `storeKey` | `String` |
| `name` | `String` |
| `weekDays` | `List<StoreDetailWeekDaysModel>` |
| `address` | `String` |
| `postalCode` | `String` |
| `locality` | `String` |
| `location` | `GeoLocationModel` |
| `state` | `String` |
| `amenities` | `List<AmenityModel>` |
| `province` | `String` |
| `countryZone` | `CountryZoneModel` |
| `showOfferRegion` | `String` |
| `zone` | `String` |

#### `stores.selector.data.models.StoreDetailOpeningHoursModel`
| JSON-Feld | Typ |
|---|---|
| `from` | `String` |
| `to` | `String` |

#### `stores.selector.data.models.StoreDetailWeekDaysModel`
| JSON-Feld | Typ |
|---|---|
| `day` | `String` |
| `isOpen` | `boolean` |
| `openingHours` | `List<StoreDetailOpeningHoursModel>` |

#### `stores.selector.data.models.StoreSearchModel`
| JSON-Feld | Typ |
|---|---|
| `storeKey` | `String` |
| `name` | `String` |
| `address` | `String` |
| `locality` | `String` |
| `distance` | `double` |
| `postalCode` | `String` |
| `location` | `GeoLocationModel` |

#### `stores.selector.data.models.WillOpenAtModel`
| JSON-Feld | Typ |
|---|---|
| `day` | `int` |
| `hour` | `String` |

#### `surveys.data.model.ActionConditionResponse`
| JSON-Feld | Typ |
|---|---|
| `operation` | `ldk` |
| `vars` | `List<ActionConditionResponse>` |
| `type` | `ayw` |
| `value` | `String` |

#### `surveys.data.model.ActionDetailsResponse`
| JSON-Feld | Typ |
|---|---|
| `to` | `ToResponse` |

#### `surveys.data.model.ActionResponse`
| JSON-Feld | Typ |
|---|---|
| `type` | `pd` |
| `details` | `ActionDetailsResponse` |
| `condition` | `ActionConditionResponse` |

#### `surveys.data.model.AnswerCompletedRequest`
| JSON-Feld | Typ |
|---|---|
| `questionId` | `String` |
| `value` | `String` |
| `order` | `Integer` |
| `skipped` | `boolean` |

#### `surveys.data.model.AnswerResponse`
| JSON-Feld | Typ |
|---|---|
| `label` | `String` |
| `value` | `String` |
| `order` | `int` |

#### `surveys.data.model.CampaignResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `introductoryTextTitle` | `String` |
| `introductoryTextDescription` | `String` |
| `endTextTitle` | `String` |
| `endTextDescription` | `String` |
| `secondaryEndTextTitle` | `String` |
| `secondaryEndTextDescription` | `String` |
| `type` | `z04` |
| `survey` | `UserSurveyResponse` |
| `url` | `String` |
| `structure` | `List<Integer>` |
| `termsAndConditions` | `String` |
| `moreInfoUrl` | `String` |

#### `surveys.data.model.CompleteUserCampaignRequest`
| JSON-Feld | Typ |
|---|---|
| `answers` | `List<AnswerCompletedRequest>` |

#### `surveys.data.model.ManualCampaignResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `introductoryTextTitle` | `String` |
| `introductoryTextDescription` | `String` |
| `endTextTitle` | `String` |
| `endTextDescription` | `String` |
| `secondaryEndTextTitle` | `String` |
| `secondaryEndTextDescription` | `String` |
| `type` | `z04` |
| `survey` | `UserSurveyResponse` |
| `status` | `o04` |
| `userStatus` | `psw` |
| `termsAndConditions` | `String` |
| `moreInfoUrl` | `String` |

#### `surveys.data.model.SurveyLogicResponse`
| JSON-Feld | Typ |
|---|---|
| `reference` | `String` |
| `actions` | `List<ActionResponse>` |

#### `surveys.data.model.SurveyQuestionResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `text` | `String` |
| `subtitle` | `String` |
| `answerType` | `ul0` |
| `answerSubtype` | `jl0` |
| `answers` | `List<AnswerResponse>` |
| `isOptional` | `boolean` |
| `imageUrl` | `String` |

#### `surveys.data.model.ToResponse`
| JSON-Feld | Typ |
|---|---|
| `type` | `g8v` |
| `value` | `String` |

#### `surveys.data.model.UserSurveyResponse`
| JSON-Feld | Typ |
|---|---|
| `questions` | `List<SurveyQuestionResponse>` |
| `logics` | `List<SurveyLogicResponse>` |

#### `tickets.data.api.models.BadgesResponse`
| JSON-Feld | Typ |
|---|---|
| `coupons` | `int` |
| `invoice` | `boolean` |
| `returns` | `int` |
| `isAvailable` | `boolean` |

#### `tickets.data.api.models.CodeLabelResponse`
| JSON-Feld | Typ |
|---|---|
| `label` | `String` |
| `isLokaliseKey` | `boolean` |
| `position` | `sj5` |

#### `tickets.data.api.models.CodeResponse`
| JSON-Feld | Typ |
|---|---|
| `code` | `String` |
| `format` | `mj5` |
| `position` | `sj5` |
| `codeType` | `bk5` |
| `size` | `vj5` |
| `label` | `CodeLabelResponse` |

#### `tickets.data.api.models.CollectingModelResponse`
| JSON-Feld | Typ |
|---|---|
| `points` | `int` |
| `pointsDate` | `OffsetDateTime` |
| `arePointsAvailable` | `boolean` |

#### `tickets.data.api.models.FiscalDataAtResponse`
| JSON-Feld | Typ |
|---|---|
| `fiscalSequenceNumber` | `String` |
| `fiscalPrinterId` | `String` |
| `fiscalBarcode` | `String` |

#### `tickets.data.api.models.FiscalDataCZResponse`
| JSON-Feld | Typ |
|---|---|
| `fiscalDataStoreTax` | `String` |
| `fiscalDataBkp` | `String` |
| `fiscalDataPkp` | `String` |
| `fiscalDataRin` | `String` |
| `fiscalDataFik` | `String` |

#### `tickets.data.api.models.FiscalDataDeResponse`
| JSON-Feld | Typ |
|---|---|
| `isActive` | `boolean` |
| `fiscalSequenceNumber` | `String` |
| `fiscalSignatureStart` | `OffsetDateTime` |
| `fiscalTimeStamp` | `OffsetDateTime` |
| `fiscalSignatureCounter` | `String` |
| `fiscalReceiptLabel` | `String` |
| `posSerialnumber` | `String` |

#### `tickets.data.api.models.GetTicketTicketForeignPaymentResponse`
| JSON-Feld | Typ |
|---|---|
| `foreignAmount` | `String` |
| `amount` | `String` |
| `foreignCurrency` | `String` |

#### `tickets.data.api.models.ReturnResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `amount` | `BigDecimal` |

#### `tickets.data.api.models.ReturnedHtmlTicketResponse`
| JSON-Feld | Typ |
|---|---|
| `ticketId` | `String` |
| `date` | `OffsetDateTime` |
| `itemsReturnedCount` | `int` |
| `fiscalBarcodeAt` | `String` |
| `htmlPrintedReceipt` | `String` |
| `codes` | `List<CodeResponse>` |

#### `tickets.data.api.models.ReturnedNativeTicketResponse`
| JSON-Feld | Typ |
|---|---|
| `ticketId` | `String` |
| `store` | `StoreResponse` |
| `sequenceNumber` | `String` |
| `workstation` | `String` |
| `date` | `OffsetDateTime` |
| `totalAmountString` | `String` |
| `totalAmount` | `BigDecimal` |
| `itemsReturned` | `List<TicketReturnedLineResponse>` |
| `taxes` | `List<TicketTaxResponse>` |
| `tenderChange` | `List<TicketTenderChangeResponse>` |
| `linesScannedCount` | `int` |
| `totalTaxes` | `TicketTotalTaxesResponse` |
| `fiscalDataAt` | `FiscalDataAtResponse` |
| `fiscalDataCZ` | `FiscalDataCZResponse` |
| `operatorId` | `String` |
| `fiscalDataDe` | `FiscalDataDeResponse` |

#### `tickets.data.api.models.StoreResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `name` | `String` |
| `address` | `String` |
| `postalCode` | `String` |
| `locality` | `String` |
| `schedule` | `String` |

#### `tickets.data.api.models.TicketCardPaymentResponse`
| JSON-Feld | Typ |
|---|---|
| `accountNumber` | `String` |

#### `tickets.data.api.models.TicketCouponResponse`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `discount` | `String` |
| `block2Description` | `String` |
| `couponTitle` | `String` |
| `couponDescription` | `String` |

#### `tickets.data.api.models.TicketCurrencyResponse`
| JSON-Feld | Typ |
|---|---|
| `code` | `String` |
| `symbol` | `String` |

#### `tickets.data.api.models.TicketDepositResponse`
| JSON-Feld | Typ |
|---|---|
| `amount` | `String` |
| `description` | `String` |
| `unitPrice` | `String` |
| `quantity` | `Integer` |
| `taxGroupName` | `String` |

#### `tickets.data.api.models.TicketDiscountResponse`
| JSON-Feld | Typ |
|---|---|
| `description` | `String` |
| `amount` | `String` |

#### `tickets.data.api.models.TicketHGAItemResponse`
| JSON-Feld | Typ |
|---|---|
| `quantity` | `int` |
| `description` | `String` |
| `grossAmount` | `BigDecimal` |

#### `tickets.data.api.models.TicketLineResponse`
| JSON-Feld | Typ |
|---|---|
| `currentUnitPrice` | `String` |
| `quantity` | `String` |
| `isWeight` | `boolean` |
| `originalAmount` | `String` |
| `name` | `String` |
| `taxGroupName` | `String` |
| `codeInput` | `String` |
| `discounts` | `List<TicketDiscountResponse>` |
| `deposit` | `TicketDepositResponse` |
| `giftSerialNumber` | `String` |

#### `tickets.data.api.models.TicketListResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `isFavorite` | `boolean` |
| `date` | `OffsetDateTime` |
| `totalAmount` | `BigDecimal` |
| `savings` | `BigDecimal` |
| `articlesCount` | `int` |
| `couponsUsedCount` | `int` |
| `returns` | `List<ReturnResponse>` |
| `isHtml` | `boolean` |
| `iconUrl` | `String` |
| `vendor` | `VendorResponse` |
| `badges` | `BadgesResponse` |
| `origin` | `TicketListResponse.a` |

#### `tickets.data.api.models.TicketListResponse.a`
Enum: `S`, `HGA`

#### `tickets.data.api.models.TicketOfferResponse`
| JSON-Feld | Typ |
|---|---|
| `offerTitle` | `String` |
| `offerDescription` | `String` |

#### `tickets.data.api.models.TicketPaymentResponse`
| JSON-Feld | Typ |
|---|---|
| `type` | `ryu` |
| `amount` | `String` |
| `description` | `String` |
| `roundingDifference` | `String` |
| `foreignPayment` | `GetTicketTicketForeignPaymentResponse` |
| `cardInfo` | `TicketCardPaymentResponse` |
| `rawPaymentInformationHTML` | `String` |

#### `tickets.data.api.models.TicketReturnedLineResponse`
| JSON-Feld | Typ |
|---|---|
| `currentUnitPrice` | `String` |
| `currentPrice` | `String` |
| `quantity` | `String` |
| `isWeight` | `boolean` |
| `amount` | `String` |
| `description` | `String` |
| `taxGroupName` | `String` |
| `codeInput` | `String` |
| `discounts` | `List<TicketDiscountResponse>` |
| `priceDifference` | `String` |
| `reason` | `String` |
| `deposit` | `TicketDepositResponse` |

#### `tickets.data.api.models.TicketTaxResponse`
| JSON-Feld | Typ |
|---|---|
| `taxGroupName` | `String` |
| `percentage` | `String` |
| `amount` | `String` |
| `taxableAmount` | `String` |
| `netAmount` | `String` |

#### `tickets.data.api.models.TicketTenderChangeResponse`
| JSON-Feld | Typ |
|---|---|
| `roundingDifference` | `String` |
| `type` | `f0v` |
| `amount` | `String` |
| `cardInfo` | `TicketCardPaymentResponse` |

#### `tickets.data.api.models.TicketTotalTaxesResponse`
| JSON-Feld | Typ |
|---|---|
| `totalAmount` | `String` |
| `totalTaxableAmount` | `String` |
| `totalNetAmount` | `String` |

#### `tickets.data.api.models.TicketUnifiedResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `ticketType` | `o0v` |
| `barCode` | `String` |
| `couponsUsed` | `List<TicketCouponResponse>` |
| `offersUsed` | `List<TicketOfferResponse>` |
| `returnedHtmlTickets` | `List<ReturnedHtmlTicketResponse>` |
| `isFavorite` | `boolean` |
| `date` | `OffsetDateTime` |
| `totalAmount` | `BigDecimal` |
| `store` | `StoreResponse` |
| `languageCode` | `String` |
| `htmlPrintedReceipt` | `String` |
| `printedReceiptState` | `TicketUnifiedResponse.a` |
| `hasInvoice` | `Boolean` |
| `sequenceNumber` | `String` |
| `workstation` | `String` |
| `itemsLine` | `List<TicketLineResponse>` |
| `taxes` | `List<TicketTaxResponse>` |
| `returnedNativeTickets` | `List<ReturnedNativeTicketResponse>` |
| `totalAmountString` | `String` |
| `currency` | `TicketCurrencyResponse` |
| `payments` | `List<TicketPaymentResponse>` |
| `tenderChange` | `List<TicketTenderChangeResponse>` |
| `isEmployee` | `Boolean` |
| `linesScannedCount` | `Integer` |
| `taxExemptTexts` | `v8u` |
| `storeID` | `String` |
| `fiscalDataAt` | `FiscalDataAtResponse` |
| `totalTaxes` | `TicketTotalTaxesResponse` |
| `fiscalDataCZ` | `FiscalDataCZResponse` |
| `fiscalDataDe` | `FiscalDataDeResponse` |
| `totalDiscount` | `String` |
| `ustIdNr` | `String` |
| `operatorId` | `String` |
| `logoUrl` | `String` |
| `watermarkUrl` | `String` |
| `codes` | `List<CodeResponse>` |
| `showCopy` | `Boolean` |
| `collectingModel` | `CollectingModelResponse` |
| `netTotalAmount` | `BigDecimal` |
| `savings` | `BigDecimal` |
| `items` | `List<TicketHGAItemResponse>` |

#### `tickets.data.api.models.TicketUnifiedResponse.a`
Enum: `UNKNOWN`, `PRINTED`, `NON_PRINTED`

#### `tickets.data.api.models.VendorResponse`
| JSON-Feld | Typ |
|---|---|
| `vendorId` | `String` |
| `vendorTransactionId` | `String` |
| `vendorLogoUrl` | `String` |

#### `tipcards.data.v1.DeviceStatusModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `status` | `String` |

#### `tipcards.data.v1.GetTipcardModel`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `type` | `String` |

#### `travel.list.data.models.Price`
| JSON-Feld | Typ |
|---|---|
| `discountMessage` | `String` |
| `discounted` | `BigDecimal` |
| `original` | `BigDecimal` |

#### `travel.list.data.models.PriceFormat`
| JSON-Feld | Typ |
|---|---|
| `currency` | `String` |
| `currencyPosition` | `hp7` |
| `decimalDelimiter` | `String` |
| `groupingSeparator` | `String` |

#### `travel.list.data.models.Travel`
| JSON-Feld | Typ |
|---|---|
| `hasAdditionalInfo` | `boolean` |
| `detailUrl` | `String` |
| `id` | `String` |
| `imageUrl` | `String` |
| `includedFlight` | `boolean` |
| `nightsCount` | `int` |
| `price` | `Price` |
| `subtitle` | `String` |
| `title` | `String` |
| `type` | `String` |

#### `travel.list.data.models.TravelListResponse`
| JSON-Feld | Typ |
|---|---|
| `listUrl` | `String` |
| `priceFormat` | `PriceFormat` |
| `travels` | `List<Travel>` |

#### `uniqueaccount.data.datasource.model.PersonalData`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `gender` | `String` |
| `firstName` | `String` |
| `surname` | `String` |
| `birthdate` | `ZonedDateTime` |

#### `wrapped.data.WrappedAssignCouponBody`
| JSON-Feld | Typ |
|---|---|
| `categoryId` | `String` |

#### `wrapped.data.WrappedModel`
| JSON-Feld | Typ |
|---|---|
| `status` | `WrappedModel.b` |
| `configuration` | `WrappedModel.Configuration` |
| `smartBuyer` | `WrappedModel.SmartBuyer` |
| `frequencyShop` | `WrappedModel.FrequencyShop` |
| `savings` | `WrappedModel.Savings` |
| `topArticles` | `WrappedModel.TopArticles` |
| `categoryPicker` | `WrappedModel.CategoryPicker` |
| `topCategories` | `WrappedModel.TopCategories` |
| `couponPlus` | `WrappedModel.CouponPlus` |
| `lidlPoints` | `WrappedModel.LidlPoints` |
| `sustainableChoices` | `WrappedModel.SustainableChoices` |
| `recognitions` | `WrappedModel.a` |
| `lottery` | `WrappedModel.Lottery` |

#### `wrapped.data.WrappedModel.Article`
| JSON-Feld | Typ |
|---|---|
| `name` | `String` |
| `tickets` | `int` |

#### `wrapped.data.WrappedModel.Category`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `position` | `int` |

#### `wrapped.data.WrappedModel.CategoryPicker`
| JSON-Feld | Typ |
|---|---|
| `categories` | `List<WrappedModel.Category>` |
| `assignedCoupon` | `String` |

#### `wrapped.data.WrappedModel.Choice`
| JSON-Feld | Typ |
|---|---|
| `type` | `WrappedModel.a` |
| `quantity` | `int` |

#### `wrapped.data.WrappedModel.Configuration`
| JSON-Feld | Typ |
|---|---|
| `hasEcommerce` | `boolean` |

#### `wrapped.data.WrappedModel.CouponPlus`
| JSON-Feld | Typ |
|---|---|
| `goalsAchieved` | `int` |

#### `wrapped.data.WrappedModel.FrequencyShop`
| JSON-Feld | Typ |
|---|---|
| `yearlyPurchases` | `int` |
| `percentile` | `int` |
| `buyerLevel` | `WrappedModel.a` |
| `months` | `List<WrappedModel.Month>` |

#### `wrapped.data.WrappedModel.LidlPoints`
| JSON-Feld | Typ |
|---|---|
| `points` | `int` |

#### `wrapped.data.WrappedModel.Lottery`
| JSON-Feld | Typ |
|---|---|
| `isLotteryParticipant` | `boolean` |
| `prizes` | `List<WrappedModel.Prize>` |
| `legalTerms` | `String` |
| `privacyNote` | `String` |

#### `wrapped.data.WrappedModel.Month`
| JSON-Feld | Typ |
|---|---|
| `id` | `int` |
| `storePurchases` | `int` |
| `onlinePurchases` | `int` |

#### `wrapped.data.WrappedModel.Prize`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `units` | `int` |
| `image` | `String` |

#### `wrapped.data.WrappedModel.SavingType`
| JSON-Feld | Typ |
|---|---|
| `used` | `int` |
| `saved` | `BigDecimal` |

#### `wrapped.data.WrappedModel.Savings`
| JSON-Feld | Typ |
|---|---|
| `totalSavings` | `BigDecimal` |
| `coupons` | `WrappedModel.SavingType` |
| `offers` | `WrappedModel.SavingType` |

#### `wrapped.data.WrappedModel.SmartBuyer`
| JSON-Feld | Typ |
|---|---|
| `smartPercent` | `int` |

#### `wrapped.data.WrappedModel.SustainableChoices`
| JSON-Feld | Typ |
|---|---|
| `choices` | `List<WrappedModel.Choice>` |

#### `wrapped.data.WrappedModel.TopArticles`
| JSON-Feld | Typ |
|---|---|
| `articles` | `List<WrappedModel.Article>` |

#### `wrapped.data.WrappedModel.TopCategories`
| JSON-Feld | Typ |
|---|---|
| `categories` | `List<WrappedModel.TopCategory>` |

#### `wrapped.data.WrappedModel.TopCategory`
| JSON-Feld | Typ |
|---|---|
| `title` | `String` |
| `percent` | `int` |

#### `wrapped.data.WrappedModel.a`
Enum: `L`, `L`, `T`, `S`, `C`, `S`

#### `wrapped.data.WrappedModel.b`
Enum: `E`, `N`, `N`

#### `es.lidlplus.literalsprovider.data.api.v1.model.LocalizationResponse`
| JSON-Feld | Typ |
|---|---|
| `country` | `String` |
| `language` | `String` |
| `version` | `String` |
| `resources` | `Map<String, String>` |

#### `eu.scrm.lidlplus.payments.eticket.data.ETicketStatusApiModel`
| JSON-Feld | Typ |
|---|---|
| `shouldPrint` | `boolean` |

#### `eu.scrm.schwarz.payments.data.api.configuration.ConfigurationFeaturesResponse`
| JSON-Feld | Typ |
|---|---|
| `name` | `String` |
| `enabled` | `boolean` |

#### `eu.scrm.schwarz.payments.data.api.configuration.ConfigurationMethodsAllowedResponse`
| JSON-Feld | Typ |
|---|---|
| `name` | `String` |
| `businessModels` | `List<String>` |
| `maxItemEnrolled` | `Integer` |
| `requiresPushNotifications` | `Boolean` |
| `image` | `String` |

#### `eu.scrm.schwarz.payments.data.api.configuration.ConfigurationResponse`
| JSON-Feld | Typ |
|---|---|
| `features` | `List<ConfigurationFeaturesResponse>` |
| `walletItems` | `List<String>` |
| `paymentMethodsAllowed` | `List<ConfigurationMethodsAllowedResponse>` |
| `cacheTTL` | `Integer` |

#### `eu.scrm.schwarz.payments.data.api.models.ErrorItemResponse`
| JSON-Feld | Typ |
|---|---|
| `type` | `String` |
| `title` | `String` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.DefaultPaymentMethodInfoResponse`
| JSON-Feld | Typ |
|---|---|
| `number` | `String` |
| `paymentType` | `PaymentTypeApi` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.GenericPaymentMethodsResponse`
| JSON-Feld | Typ |
|---|---|
| `paymentMethods` | `List<GenericPaymentMethodResponse>` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.QrRequest`
| JSON-Feld | Typ |
|---|---|
| `loyaltyId` | `String` |
| `paymentMethodId` | `String` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.QrResponse`
| JSON-Feld | Typ |
|---|---|
| `paymentQR` | `String` |
| `creditLimit` | `BigDecimal` |
| `currency` | `String` |
| `errors` | `List<ErrorItemResponse>` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.SepaPaymentLimitResponse`
| JSON-Feld | Typ |
|---|---|
| `creditLimit` | `BigDecimal` |
| `currency` | `String` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.SetPaymentMethodRequest`
| JSON-Feld | Typ |
|---|---|
| `paymentMethodId` | `String` |
| `alias` | `String` |
| `isDefault` | `boolean` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.SubscriptionResponse`
| JSON-Feld | Typ |
|---|---|
| `name` | `String` |
| `iconUrl` | `String` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.SubscriptionsResponse`
| JSON-Feld | Typ |
|---|---|
| `subscriptions` | `List<SubscriptionResponse>` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.TransactionResponse`
| JSON-Feld | Typ |
|---|---|
| `date` | `OffsetDateTime` |
| `title` | `String` |
| `amount` | `BigDecimal` |
| `currency` | `String` |
| `icon` | `String` |
| `country` | `String` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.TransactionsResponse`
| JSON-Feld | Typ |
|---|---|
| `transactions` | `List<TransactionResponse>` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.ValidateDefaultPaymentMethodData`
| JSON-Feld | Typ |
|---|---|
| `defaultPaymentMethodInfo` | `String` |

#### `eu.scrm.schwarz.payments.data.api.paymentmethods.ValidateDefaultPaymentMethodInfoResponse`
| JSON-Feld | Typ |
|---|---|
| `status` | `ValidateDefaultPaymentMethodInfoStatusResponse` |
| `remainingAttempts` | `int` |

#### `eu.scrm.schwarz.payments.data.api.profile.ActivateRequest`
| JSON-Feld | Typ |
|---|---|
| `isActive` | `boolean` |

#### `eu.scrm.schwarz.payments.data.api.profile.ActivateResult`
| JSON-Feld | Typ |
|---|---|
| `hasLidlPayActive` | `boolean` |

#### `eu.scrm.schwarz.payments.data.api.profile.AddressRequest`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `country` | `String` |
| `street` | `String` |
| `number` | `String` |
| `door` | `String` |
| `postCode` | `String` |
| `city` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.ChangePinRequest`
| JSON-Feld | Typ |
|---|---|
| `pin` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.CreatePinRequest`
| JSON-Feld | Typ |
|---|---|
| `pin` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.CreateProfileRequest`
| JSON-Feld | Typ |
|---|---|
| `favoriteStore` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.ForgotPinRequest`
| JSON-Feld | Typ |
|---|---|
| `pin` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.GenericPaymentMethodResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `status` | `String` |
| `number` | `String` |
| `alias` | `String` |
| `brand` | `String` |
| `isDefault` | `boolean` |
| `type` | `String` |
| `defaultInBusinessModel` | `List<String>` |
| `bankName` | `String` |
| `accountHolder` | `String` |
| `icon` | `String` |
| `cardBackgroundImage` | `String` |
| `balance` | `BigDecimal` |
| `minTopUpAmount` | `BigDecimal` |
| `maxTopUpAmount` | `BigDecimal` |
| `currency` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.IsMailSentResult`
| JSON-Feld | Typ |
|---|---|
| `isMailSent` | `boolean` |

#### `eu.scrm.schwarz.payments.data.api.profile.IsMailVerifiedResult`
| JSON-Feld | Typ |
|---|---|
| `isMailVerified` | `boolean` |

#### `eu.scrm.schwarz.payments.data.api.profile.PaymentProfileResponse`
| JSON-Feld | Typ |
|---|---|
| `status` | `String` |
| `addressId` | `String` |
| `countryHasOnlyStore` | `boolean` |
| `hasLidlPayActive` | `boolean` |
| `paymentMethods` | `List<GenericPaymentMethodResponse>` |

#### `eu.scrm.schwarz.payments.data.api.profile.ValidateOTPRequest`
| JSON-Feld | Typ |
|---|---|
| `otp` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.ValidateOTPResultResponse`
| JSON-Feld | Typ |
|---|---|
| `token` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.ValidatePinRequest`
| JSON-Feld | Typ |
|---|---|
| `pin` | `String` |

#### `eu.scrm.schwarz.payments.data.api.profile.ValidatePinResult`
| JSON-Feld | Typ |
|---|---|
| `status` | `PinValidationStatusResponse` |
| `failedAttempts` | `int` |
| `token` | `String` |

#### `eu.scrm.schwarz.payments.data.api.psp.AddBalanceErrorResponse`
| JSON-Feld | Typ |
|---|---|
| `message` | `String` |
| `type` | `String` |
| `points` | `Integer` |

#### `eu.scrm.schwarz.payments.data.api.psp.AddBalanceRequest`
| JSON-Feld | Typ |
|---|---|
| `paymentMethodIdUsedFor` | `String` |
| `amount` | `double` |

#### `eu.scrm.schwarz.payments.data.api.psp.AddBalanceResponse`
| JSON-Feld | Typ |
|---|---|
| `balance` | `Double` |
| `status` | `String` |
| `currency` | `String` |
| `redirectUrl` | `String` |
| `errors` | `List<AddBalanceErrorResponse>` |
| `points` | `Integer` |

#### `eu.scrm.schwarz.payments.data.api.psp.LastAcceptedResponse`
| JSON-Feld | Typ |
|---|---|
| `bankTransactionId` | `String` |
| `currency` | `String` |
| `cardNo` | `String` |
| `date` | `String` |
| `hour` | `String` |
| `merchantCode` | `String` |
| `terminal` | `String` |
| `till` | `String` |
| `authorizationCode` | `String` |
| `validationCode` | `String` |
| `totalSum` | `double` |

#### `eu.scrm.schwarz.payments.data.api.psp.PaymentTypeEnrollmentResponse`
| JSON-Feld | Typ |
|---|---|
| `status` | `String` |
| `transactionId` | `String` |
| `enrollmentUrl` | `String` |
| `scaUrls` | `List<String>` |

#### `eu.scrm.schwarz.payments.data.api.psp.PollingTransactionStatusResponse`
| JSON-Feld | Typ |
|---|---|
| `status` | `String` |

#### `eu.scrm.schwarz.payments.data.api.psp.PreAuthStandardRequest`
| JSON-Feld | Typ |
|---|---|
| `paymentMethodId` | `String` |
| `preAuthRequestId` | `String` |

#### `eu.scrm.schwarz.payments.data.api.psp.PreAuthStandardResponse`
| JSON-Feld | Typ |
|---|---|
| `businessModelTransactionId` | `String` |
| `status` | `String` |
| `amount` | `String` |
| `currency` | `String` |
| `redirectUrl` | `String` |
| `successUrl` | `String` |
| `errorUrl` | `String` |
| `cancelUrl` | `String` |

#### `eu.scrm.schwarz.payments.data.api.uniqueaccount.AddressListResponse`
| JSON-Feld | Typ |
|---|---|
| `addresses` | `List<AddressResponse>` |

#### `eu.scrm.schwarz.payments.data.api.uniqueaccount.AddressResponse`
| JSON-Feld | Typ |
|---|---|
| `id` | `String` |
| `lastUpdate` | `String` |
| `country` | `String` |
| `city` | `String` |
| `street` | `String` |
| `number` | `String` |
| `door` | `String` |
| `postcode` | `String` |
| `isDefault` | `Boolean` |
| `fullName` | `String` |
| `isCompleted` | `Boolean` |
