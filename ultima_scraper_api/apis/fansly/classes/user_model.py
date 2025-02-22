from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, Optional, Union
from urllib import parse

import ultima_scraper_api.apis.fansly.classes.message_model as message_model
from ultima_scraper_api.apis import api_helper
from ultima_scraper_api.apis.fansly.classes import collection_model, post_model
from ultima_scraper_api.apis.fansly.classes.extras import (
    ErrorDetails,
    endpoint_links,
    handle_refresh,
)
from ultima_scraper_api.apis.fansly.classes.hightlight_model import create_highlight
from ultima_scraper_api.apis.fansly.classes.story_model import create_story
from ultima_scraper_api.apis.user_streamliner import StreamlinedUser
from ultima_scraper_api.managers.scrape_manager import ScrapeManager

if TYPE_CHECKING:
    from ultima_scraper_api.apis.fansly.classes.auth_model import AuthModel
    from ultima_scraper_api.apis.fansly.classes.post_model import create_post


class create_user(StreamlinedUser):
    def __init__(
        self,
        option: dict[str, Any],
        authed: AuthModel,
    ) -> None:
        self.avatar: Any = option.get("avatar")
        self.avatarThumbs: Any = option.get("avatarThumbs")
        self.header: Any = option.get("banner")
        self.headerSize: Any = option.get("headerSize")
        self.headerThumbs: Any = option.get("headerThumbs")
        self.id: int = int(option.get("id", 9001))
        self.name: str = option.get("name")
        self.username: str = option.get("username")
        self.canLookStory: bool = option.get("canLookStory")
        self.canCommentStory: bool = option.get("canCommentStory")
        self.hasNotViewedStory: bool = option.get("hasNotViewedStory")
        self.isVerified: bool = option.get("isVerified")
        self.canPayInternal: bool = option.get("canPayInternal")
        self.hasScheduledStream: bool = option.get("hasScheduledStream")
        self.hasStream: bool = option.get("hasStream")
        self.hasStories: bool = option.get("hasStories")
        self.tipsEnabled: bool = option.get("tipsEnabled")
        self.tipsTextEnabled: bool = option.get("tipsTextEnabled")
        self.tipsMin: int = option.get("tipsMin")
        self.tipsMax: int = option.get("tipsMax")
        self.canEarn: bool = option.get("canEarn")
        self.canAddSubscriber: bool = option.get("canAddSubscriber")
        self.subscribePrice: int = option.get("subscribePrice")
        self.hasStripe: bool = option.get("hasStripe")
        self.isStripeExist: bool = option.get("isStripeExist")
        self.subscriptionBundles: list[dict[Any, Any]] = option.get(
            "subscriptionTiers", []
        )
        self.canSendChatToAll: bool = option.get("canSendChatToAll")
        self.creditsMin: int = option.get("creditsMin")
        self.creditsMax: int = option.get("creditsMax")
        self.isPaywallRestriction: bool = option.get("isPaywallRestriction")
        self.unprofitable: bool = option.get("unprofitable")
        self.listsSort: str = option.get("listsSort")
        self.listsSortOrder: str = option.get("listsSortOrder")
        self.canCreateLists: bool = option.get("canCreateLists")
        self.joinDate: str = option.get("joinDate")
        self.isReferrerAllowed: bool = option.get("isReferrerAllowed")
        self.about: str = option.get("about")
        self.rawAbout: str = option.get("rawAbout")
        self.website: str = option.get("website")
        self.wishlist: str = option.get("wishlist")
        self.location: str = option.get("location")
        timeline_stats = option.get("timelineStats", {})
        self.postsCount: int = option.get("postsCount", 0)
        self.archivedPostsCount: int = option.get("archivedPostsCount", 0)
        self.photosCount: int = timeline_stats.get("imageCount", 0)
        self.videosCount: int = timeline_stats.get("videoCount", 0)
        self.audiosCount: int = option.get("audiosCount", 0)
        self.mediasCount: int = option.get("mediasCount", 0)
        self.promotions: list = option.get("promotions")
        self.lastSeen: Any = option.get("lastSeen")
        self.favoritedCount: int = option.get("accountMediaLikes")
        self.showPostsInFeed: bool = option.get("showPostsInFeed")
        self.canReceiveChatMessage: bool = option.get("canReceiveChatMessage")
        self.isPerformer: bool = bool(self.subscriptionBundles)
        self.isRealPerformer: bool = option.get("isRealPerformer")
        self.isSpotifyConnected: bool = option.get("isSpotifyConnected")
        self.subscribersCount: int = option.get("subscribersCount")
        self.hasPinnedPosts: bool = option.get("hasPinnedPosts")
        self.canChat: bool = option.get("canChat")
        self.callPrice: int = option.get("callPrice")
        self.isPrivateRestriction: bool = option.get("isPrivateRestriction")
        self.following: bool = option.get("following")
        self.showSubscribersCount: bool = option.get("showSubscribersCount")
        self.showMediaCount: bool = option.get("showMediaCount")
        self.subscribed: bool = option.get("subscribed", False)
        self.subscribedByData: Any = option.get("subscription")
        self.subscribedOnData: Any = option.get("subscribedOnData")
        self.canPromotion: bool = option.get("canPromotion")
        self.canCreatePromotion: bool = option.get("canCreatePromotion")
        self.canCreateTrial: bool = option.get("canCreateTrial")
        self.isAdultContent: bool = option.get("isAdultContent")
        self.isBlocked: bool = option.get("isBlocked")
        self.canTrialSend: bool = option.get("canTrialSend")
        self.canAddPhone: bool = option.get("canAddPhone")
        self.phoneLast4: Any = option.get("phoneLast4")
        self.phoneMask: Any = option.get("phoneMask")
        self.hasNewTicketReplies: dict = option.get("hasNewTicketReplies")
        self.hasInternalPayments: bool = option.get("hasInternalPayments")
        self.isCreditsEnabled: bool = option.get("isCreditsEnabled")
        self.creditBalance: float = (
            option["mainWallet"]["balance"] if "mainWallet" in option else 0
        )
        self.isMakePayment: bool = option.get("isMakePayment")
        self.isOtpEnabled: bool = option.get("isOtpEnabled")
        self.email: str = option.get("email")
        self.isEmailChecked: bool = option.get("isEmailChecked")
        self.isLegalApprovedAllowed: bool = option.get("isLegalApprovedAllowed")
        self.isTwitterConnected: bool = option.get("isTwitterConnected")
        self.twitterUsername: Any = option.get("twitterUsername")
        self.isAllowTweets: bool = option.get("isAllowTweets")
        self.isPaymentCardConnected: bool = option.get("isPaymentCardConnected")
        self.referalUrl: str = option.get("referalUrl")
        self.isVisibleOnline: bool = option.get("isVisibleOnline")
        self.subscribesCount: int = option.get("subscribesCount")
        self.canPinPost: bool = option.get("canPinPost")
        self.hasNewAlerts: bool = option.get("hasNewAlerts")
        self.hasNewHints: bool = option.get("hasNewHints")
        self.hasNewChangedPriceSubscriptions: bool = option.get(
            "hasNewChangedPriceSubscriptions"
        )
        self.notificationsCount: int = option.get("notificationsCount")
        self.chatMessagesCount: int = option.get("chatMessagesCount")
        self.isWantComments: bool = option.get("isWantComments")
        self.watermarkText: str = option.get("watermarkText")
        self.customWatermarkText: Any = option.get("customWatermarkText")
        self.hasWatermarkPhoto: bool = option.get("hasWatermarkPhoto")
        self.hasWatermarkVideo: bool = option.get("hasWatermarkVideo")
        self.canDelete: bool = option.get("canDelete")
        self.isTelegramConnected: bool = option.get("isTelegramConnected")
        self.advBlock: list = option.get("advBlock")
        self.hasPurchasedPosts: bool = option.get("hasPurchasedPosts")
        self.isEmailRequired: bool = option.get("isEmailRequired")
        self.isPayoutLegalApproved: bool = option.get("isPayoutLegalApproved")
        self.payoutLegalApproveState: str = option.get("payoutLegalApproveState")
        self.payoutLegalApproveRejectReason: Any = option.get(
            "payoutLegalApproveRejectReason"
        )
        self.enabledImageEditorForChat: bool = option.get("enabledImageEditorForChat")
        self.shouldReceiveLessNotifications: bool = option.get(
            "shouldReceiveLessNotifications"
        )
        self.canCalling: bool = option.get("canCalling")
        self.paidFeed: bool = option.get("paidFeed")
        self.canSendSms: bool = option.get("canSendSms")
        self.canAddFriends: bool = option.get("canAddFriends")
        self.isRealCardConnected: bool = option.get("isRealCardConnected")
        self.countPriorityChat: int = option.get("countPriorityChat")
        self.hasScenario: bool = option.get("hasScenario")
        self.isWalletAutorecharge: bool = option.get("isWalletAutorecharge")
        self.walletAutorechargeAmount: int = option.get("walletAutorechargeAmount")
        self.walletAutorechargeMin: int = option.get("walletAutorechargeMin")
        self.walletFirstRebills: bool = option.get("walletFirstRebills")
        self.closeFriends: int = option.get("closeFriends")
        self.canAlternativeWalletTopUp: bool = option.get("canAlternativeWalletTopUp")
        self.needIVApprove: bool = option.get("needIVApprove")
        self.ivStatus: Any = option.get("ivStatus")
        self.ivFailReason: Any = option.get("ivFailReason")
        self.canCheckDocsOnAddCard: bool = option.get("canCheckDocsOnAddCard")
        self.faceIdAvailable: bool = option.get("faceIdAvailable")
        self.ivCountry: Any = option.get("ivCountry")
        self.ivForcedVerified: bool = option.get("ivForcedVerified")
        self.ivFlow: str = option.get("ivFlow")
        self.isVerifiedReason: bool = option.get("isVerifiedReason")
        self.canReceiveManualPayout: bool = option.get("canReceiveManualPayout")
        self.canReceiveStripePayout: bool = option.get("canReceiveStripePayout")
        self.manualPayoutPendingDays: int = option.get("manualPayoutPendingDays")
        self.isNeedConfirmPayout: bool = option.get("isNeedConfirmPayout")
        self.canStreaming: bool = option.get("canStreaming")
        self.isScheduledStreamsAllowed: bool = option.get("isScheduledStreamsAllowed")
        self.canMakeExpirePosts: bool = option.get("canMakeExpirePosts")
        self.trialMaxDays: int = option.get("trialMaxDays")
        self.trialMaxExpiresDays: int = option.get("trialMaxExpiresDays")
        self.messageMinPrice: int = option.get("messageMinPrice")
        self.messageMaxPrice: int = option.get("messageMaxPrice")
        self.postMinPrice: int = option.get("postMinPrice")
        self.postMaxPrice: int = option.get("postMaxPrice")
        self.streamMinPrice: int = option.get("streamMinPrice")
        self.streamMaxPrice: int = option.get("streamMaxPrice")
        self.canCreatePaidStream: bool = option.get("canCreatePaidStream")
        self.callMinPrice: int = option.get("callMinPrice")
        self.callMaxPrice: int = option.get("callMaxPrice")
        self.subscribeMinPrice: float = option.get("subscribeMinPrice")
        self.subscribeMaxPrice: int = option.get("subscribeMaxPrice")
        self.bundleMaxPrice: int = option.get("bundleMaxPrice")
        self.unclaimedOffersCount: int = option.get("unclaimedOffersCount")
        self.claimedOffersCount: int = option.get("claimedOffersCount")
        self.withdrawalPeriod: str = option.get("withdrawalPeriod")
        self.canAddStory: bool = option.get("canAddStory")
        self.canAddSubscriberByBundle: bool = option.get("canAddSubscriberByBundle")
        self.isSuggestionsOptOut: bool = option.get("isSuggestionsOptOut")
        self.canCreateFundRaising: bool = option.get("canCreateFundRaising")
        self.minFundRaisingTarget: int = option.get("minFundRaisingTarget")
        self.maxFundRaisingTarget: int = option.get("maxFundRaisingTarget")
        self.disputesRatio: int = option.get("disputesRatio")
        self.vaultListsSort: str = option.get("vaultListsSort")
        self.vaultListsSortOrder: str = option.get("vaultListsSortOrder")
        self.canCreateVaultLists: bool = option.get("canCreateVaultLists")
        self.canMakeProfileLinks: bool = option.get("canMakeProfileLinks")
        self.replyOnSubscribe: bool = option.get("replyOnSubscribe")
        self.payoutType: str = option.get("payoutType")
        self.minPayoutSumm: int = option.get("minPayoutSumm")
        self.canHasW9Form: bool = option.get("canHasW9Form")
        self.isVatRequired: bool = option.get("isVatRequired")
        self.isCountryVatRefundable: bool = option.get("isCountryVatRefundable")
        self.isCountryVatNumberCollect: bool = option.get("isCountryVatNumberCollect")
        self.vatNumberName: str = option.get("vatNumberName")
        self.isCountryWithVat: bool = option.get("isCountryWithVat")
        self.connectedOfAccounts: list = option.get("connectedOfAccounts")
        self.hasPassword: bool = option.get("hasPassword")
        self.canConnectOfAccount: bool = option.get("canConnectOfAccount")
        self.pinnedPostsCount: int = option.get("pinnedPostsCount")
        self.maxPinnedPostsCount: int = option.get("maxPinnedPostsCount")
        # Custom
        authed.users.add(self)
        self.download_info: dict[str, Any] = {}
        self.duplicate_media = []
        self.scrape_manager = ScrapeManager(authed.session_manager)
        self.__raw__ = option
        self.__db_user__: Any = None
        StreamlinedUser.__init__(self, authed)

    def get_username(self):
        return self.username

    def get_link(self):
        link = f"https://fansly.com/{self.username}"
        return link

    def is_me(self) -> bool:
        status = False
        if self.email:
            status = True
        return status

    def is_authed_user(self):
        if self.id == self.get_authed().id:
            return True
        else:
            return False

    async def get_stories(
        self, refresh: bool = True, limit: int = 100, offset: int = 0
    ) -> list[create_story]:
        result, status = await api_helper.default_data(self, refresh)
        if status:
            return result
        link = [
            endpoint_links(
                identifier=self.id, global_limit=limit, global_offset=offset
            ).stories_api
        ]
        return []
        results = await api_helper.scrape_endpoint_links(
            link, self.get_session_manager()
        )
        results = [create_story(x) for x in results]
        self.temp_scraped.Stories = results
        return results

    async def get_highlights(
        self, identifier="", refresh=True, limit=100, offset=0, hightlight_id=""
    ) -> list:
        api_type = "highlights"
        if not refresh:
            result = handle_refresh(self, api_type)
            if result:
                return result
        if not identifier:
            identifier = self.id
        if not hightlight_id:
            link = endpoint_links(
                identifier=identifier, global_limit=limit, global_offset=offset
            ).list_highlights
            results = await self.session_manager.json_request(link)
            results = await remove_errors(results)
            results = [create_highlight(x) for x in results]
        else:
            link = endpoint_links(
                identifier=hightlight_id, global_limit=limit, global_offset=offset
            ).highlight
            results = await self.session_manager.json_request(link)
            results = [create_story(x) for x in results["stories"]]
        return results

    async def get_posts(
        self,
        links: Optional[list[str]] = None,
        limit: int = 10,
        offset: int = 0,
        refresh: bool = True,
    ) -> list[create_post]:
        result, status = await api_helper.default_data(self, refresh)
        if status:
            return result
        temp_results: list[Any] = []
        while True:
            link = endpoint_links(identifier=self.id, global_offset=offset).post_api
            response = await self.get_session_manager().json_request(link)
            data = response["response"]
            temp_posts = data.get("posts")
            if not temp_posts:
                break
            offset = temp_posts[-1]["id"]
            temp_results.append(data)
        results = api_helper.merge_dictionaries(temp_results)
        final_results = []
        if results:
            final_results = [
                post_model.create_post(x, self, results) for x in results["posts"]
            ]
            for result in final_results:
                await result.get_comments()
            self.scrape_manager.scraped.Posts = final_results
        return final_results

    async def get_post(
        self, identifier: Optional[int | str] = None, limit: int = 10, offset: int = 0
    ) -> Union[create_post, ErrorDetails]:
        if not identifier:
            identifier = self.id
        link = endpoint_links(
            identifier=identifier, global_limit=limit, global_offset=offset
        ).post_by_id
        result = await self.get_session_manager().json_request(link)
        if isinstance(result, dict):
            temp_result: dict[str, Any] = result
            final_result = post_model.create_post(temp_result, self, temp_result)
            return final_result
        return result

    async def get_groups(self) -> ErrorDetails | dict[str, Any]:
        link = endpoint_links().groups_api
        response: ErrorDetails | dict[
            str, Any
        ] = await self.get_session_manager().json_request(link)
        if isinstance(response, dict):
            final_response: dict[str, Any] = response["response"]
            return final_response
        return response

    async def get_messages(
        self,
        links: Optional[list[str]] = None,
        limit: int = 100000,
        before: str = "",
        cutoff_id: int | None = None,
        refresh: bool = True,
        inside_loop: bool = False,
    ):
        result, status = await api_helper.default_data(self, refresh)
        if status:
            return result
        groups = await self.get_groups()
        if isinstance(groups, ErrorDetails):
            return []
        found_id: Optional[int] = None
        for group in groups["groups"]:
            for user in group["users"]:
                if self.id == int(user["userId"]):
                    found_id = int(user["groupId"])
                    break
        final_results: list[message_model.create_message] = []
        if found_id:
            if links is None:
                links = []

            link = endpoint_links(
                identifier=found_id, global_limit=limit, before_id=before
            ).message_api
            links.append(link)

            results = await self.get_session_manager().bulk_requests(links)
            results = [await x.json() for x in results if x]
            results = await api_helper.remove_errors(results)
            results = api_helper.merge_dictionaries(results)
            if not results:
                return []
            extras = results["response"]
            final_results = extras["messages"]

            if final_results:
                lastId = final_results[-1]["id"]
                results2 = await self.get_messages(
                    links=[links[-1]],
                    limit=limit,
                    before=lastId,
                    inside_loop=True,
                )
                final_results.extend(results2)
            if not inside_loop:
                final_results = [
                    message_model.create_message(x, self, extras)
                    for x in final_results
                    if x
                ]
            self.scrape_manager.scraped.Messages = final_results
        return final_results

    async def get_message_by_id(
        self, user_id=None, message_id=None, refresh=True, limit=10, offset=0
    ):
        if not user_id:
            user_id = self.id
        link = endpoint_links(
            identifier=user_id,
            identifier2=message_id,
            global_limit=limit,
            global_offset=offset,
        ).message_by_id
        response = await self.session_manager.json_request(link)
        if isinstance(response, dict):
            results = [x for x in response["list"] if x["id"] == message_id]
            result = results[0] if results else {}
            final_result = message_model.create_message(result, self)
            return final_result
        return response

    async def get_archived_stories(
        self, refresh: bool = True, limit: int = 100, offset: int = 0
    ):
        result, status = await api_helper.default_data(self, refresh)
        if status:
            return result
        link = endpoint_links(global_limit=limit, global_offset=offset).archived_stories
        results = await self.get_session_manager().json_request(link)
        results = await api_helper.remove_errors(results)
        results = [create_story(x) for x in results]
        return results

    async def get_archived_posts(
        self,
        links: Optional[list[str]] = None,
        refresh: bool = True,
        limit: int = 10,
        offset: int = 0,
    ):
        result, status = await api_helper.default_data(self, refresh)
        if status:
            return result
        if links is None:
            links = []
        api_count = self.archivedPostsCount
        if api_count and not links:
            link = endpoint_links(
                identifier=self.id, global_limit=limit, global_offset=offset
            ).archived_posts
            ceil = math.ceil(api_count / limit)
            numbers = list(range(ceil))
            for num in numbers:
                num = num * limit
                link = link.replace(f"limit={limit}", f"limit={limit}")
                new_link = link.replace("offset=0", f"offset={num}")
                links.append(new_link)
        results = await self.scrape_manager.bulk_scrape(links)
        final_results = self.finalize_content_set(results)

        self.temp_scraped.Archived.Posts = final_results
        return final_results

    async def get_archived(self, api):
        items = []
        if self.is_me():
            item = {}
            item["type"] = "Stories"
            item["results"] = [await self.get_archived_stories()]
            items.append(item)
        item = {}
        item["type"] = "Posts"
        # item["results"] = test
        item["results"] = await self.get_archived_posts()
        items.append(item)
        return items

    async def search_chat(
        self, identifier="", text="", refresh=True, limit=10, offset=0
    ):
        if identifier:
            identifier = parse.urljoin(identifier, "messages")
        link = endpoint_links(
            identifier=identifier, text=text, global_limit=limit, global_offset=offset
        ).search_chat
        results = await self.session_manager.json_request(link)
        return results

    async def search_messages(
        self, identifier="", text="", refresh=True, limit=10, offset=0
    ):
        if identifier:
            identifier = parse.urljoin(identifier, "messages")
        text = parse.quote_plus(text)
        link = endpoint_links(
            identifier=identifier, text=text, global_limit=limit, global_offset=offset
        ).search_messages
        results = await self.session_manager.json_request(link)
        return results

    async def like(self, category: str, identifier: int):
        link = endpoint_links(identifier=category, identifier2=identifier).like
        results = await self.session_manager.json_request(link, method="POST")
        return results

    async def unlike(self, category: str, identifier: int):
        link = endpoint_links(identifier=category, identifier2=identifier).like
        results = await self.session_manager.json_request(link, method="DELETE")
        return results

    async def subscription_price(self):
        """
        Returns subscription price. This includes the promotional price.
        """
        for bundle in self.subscriptionBundles:
            return bundle["price"] / 1000

    async def buy_subscription(self):
        """
        This function will subscribe to a model. If the model has a promotion available, it will use it.
        """
        subscription_price = await self.subscription_price()
        x = {
            "paymentType": "subscribe",
            "userId": self.id,
            "subscribeSource": "profile",
            "amount": subscription_price,
            "token": "",
            "unavailablePaymentGates": [],
        }
        if self.subscriber.creditBalance >= subscription_price:
            link = endpoint_links().pay
            result = await self.session_manager.json_request(
                link, method="POST", payload=x
            )
        else:
            result = ErrorDetails(
                {"code": 2011, "message": "Insufficient Credit Balance"}
            )
        return result

    def finalize_content_set(self, results: list[dict[str, Any]] | list[str]):
        final_results: list[create_post] = []
        for result in results:
            if isinstance(result, str):
                continue
            content_type = result["responseType"]
            match content_type:
                case "post":
                    created = post_model.create_post(result, self)
                    final_results.append(created)
                case _:
                    print
        return final_results

    async def if_scraped(self):
        status = False
        for key, value in self.scrape_manager.scraped.__dict__.items():
            if key == "Archived":
                for _key_2, value in value.__dict__.items():
                    if value:
                        status = True
                        return status
            if value:
                status = True
                break
        return status

    async def match_identifiers(self, identifiers: list[int | str]):
        if self.id in identifiers or self.username in identifiers:
            return True
        else:
            return False

    async def get_collections(self):
        link = endpoint_links(identifier=self.id).collections_api
        results = await self.get_session_manager().json_request(link)
        return results["response"]

    async def get_collection_content(self, collection: dict[str, Any], offset: int = 0):
        temp_responses: list[dict[str, Any]] = []
        while True:
            link = endpoint_links(
                identifier=collection["id"], global_limit=25, global_offset=offset
            ).collection_api
            results = await self.get_session_manager().json_request(link)
            response = results["response"]
            album_content = response["albumContent"]
            if not album_content:
                break
            offset = int(album_content[-1]["id"])
            temp_responses.append(response)
        responses = api_helper.merge_dictionaries(temp_responses)
        final_result = collection_model.create_collection(collection, self, responses)
        return final_result

    async def get_avatar(self):
        return self.avatar["locations"][0]["location"] if self.header else None

    async def get_header(self):
        return self.header["locations"][0]["location"] if self.header else None

    async def is_subscribed(self):
        pass
