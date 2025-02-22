from __future__ import annotations

import math
from itertools import chain
from typing import TYPE_CHECKING, Any, Optional, Union
from urllib import parse

import ultima_scraper_api.apis.onlyfans.classes.message_model as message_model
from ultima_scraper_api.apis import api_helper
from ultima_scraper_api.apis.onlyfans.classes import post_model
from ultima_scraper_api.apis.onlyfans.classes.extras import ErrorDetails, endpoint_links
from ultima_scraper_api.apis.onlyfans.classes.hightlight_model import create_highlight
from ultima_scraper_api.apis.onlyfans.classes.story_model import create_story
from ultima_scraper_api.apis.user_streamliner import StreamlinedUser
from ultima_scraper_api.managers.scrape_manager import ScrapeManager

if TYPE_CHECKING:
    from ultima_scraper_api.apis.onlyfans.classes.auth_model import AuthModel
    from ultima_scraper_api.apis.onlyfans.classes.post_model import create_post


class create_user(StreamlinedUser):
    def __init__(self, option: dict[str, Any], authed: AuthModel) -> None:
        self.avatar: Optional[str] = option.get("avatar")
        self.avatarThumbs: Optional[list[str]] = option.get("avatarThumbs")
        self.header: Optional[str] = option.get("header")
        self.headerSize: Optional[dict[str, int]] = option.get("headerSize")
        self.headerThumbs: Optional[list[str]] = option.get("headerThumbs")
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
        self.is_deleted: bool | None = option.get("isDeleted", None)
        self.hasStripe: bool = option.get("hasStripe")
        self.isStripeExist: bool = option.get("isStripeExist")
        self.subscriptionBundles: list = option.get("subscriptionBundles")
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
        self.postsCount: int = option.get("postsCount", 0)
        self.archivedPostsCount: int = option.get("archivedPostsCount", 0)
        self.photosCount: int = option.get("photosCount", 0)
        self.videosCount: int = option.get("videosCount", 0)
        self.audiosCount: int = option.get("audiosCount", 0)
        self.mediasCount: int = option.get("mediasCount", 0)
        self.promotions: list[dict[str, Any]] = option.get("promotions", {})
        self.lastSeen: Any = option.get("lastSeen")
        self.favoritesCount: int = option.get("favoritesCount", 0)
        self.favoritedCount: int = option.get("favoritedCount", 0)
        self.showPostsInFeed: bool = option.get("showPostsInFeed")
        self.canReceiveChatMessage: bool = option.get("canReceiveChatMessage")
        self.isPerformer: bool = option.get("isPerformer", False)
        self.isRealPerformer: bool = option.get("isRealPerformer")
        self.isSpotifyConnected: bool = option.get("isSpotifyConnected")
        self.subscribersCount: int = option.get("subscribersCount")
        self.hasPinnedPosts: bool = option.get("hasPinnedPosts")
        self.canChat: bool = option.get("canChat")
        self.callPrice: int = option.get("callPrice")
        self.isPrivateRestriction: bool = option.get("isPrivateRestriction")
        self.showSubscribersCount: bool = option.get("showSubscribersCount")
        self.showMediaCount: bool = option.get("showMediaCount")
        self.subscribedByData: Any = option.get("subscribedByData")
        self.subscribedOnData: Any = option.get("subscribedOnData")
        self.subscribedIsExpiredNow: bool = option.get("subscribedIsExpiredNow")
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
        self.creditBalance: float = option.get("creditBalance", 0.0)
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
        self.subscribesCount: int = option.get("subscribesCount", 0)
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
        self.username = self.get_username()
        self.download_info: dict[str, Any] = {}
        self.duplicate_media = []
        self.scrape_manager = ScrapeManager(authed.session_manager)
        self.__raw__ = option
        self.__db_user__: Any = None
        StreamlinedUser.__init__(self, authed)

    def get_username(self):
        if not self.username:
            self.username = f"u{self.id}"
        return self.username

    def get_link(self):
        link = f"https://onlyfans.com/{self.username}"
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
        links = [
            endpoint_links(
                identifier=self.id, global_limit=limit, global_offset=offset
            ).stories_api
        ]

        results = await self.scrape_manager.bulk_scrape(links)
        final_results = [create_story(x, self) for x in results]
        self.scrape_manager.scraped.Stories = final_results
        return final_results

    async def get_highlights(
        self,
        identifier: int | str = "",
        refresh: bool = True,
        limit: int = 100,
        offset: int = 0,
        hightlight_id: int | str = "",
    ) -> list[create_highlight] | list[create_story]:
        from ultima_scraper_api import error_types

        default_result, status = await api_helper.default_data(self, refresh)
        if status:
            return default_result
        final_results = []
        if not identifier:
            identifier = self.id
        if not hightlight_id:
            link = endpoint_links(
                identifier=identifier, global_limit=limit, global_offset=offset
            ).list_highlights
            result: dict[str, Any] = await self.get_session_manager().json_request(link)
            final_results = [create_highlight(x, self) for x in result.get("list", [])]
        else:
            link = endpoint_links(
                identifier=hightlight_id, global_limit=limit, global_offset=offset
            ).highlight
            result = await self.get_session_manager().json_request(link)
            if not isinstance(result, error_types):
                final_results = [create_story(x, self) for x in result["stories"]]
        return final_results

    async def get_posts(
        self,
        links: Optional[list[str]] = None,
        limit: int = 50,
        offset: int = 0,
        refresh: bool = True,
    ) -> list[create_post]:
        result, status = await api_helper.default_data(self, refresh)
        if status:
            return result
        if links is None:
            links = []
        if not links:
            epl = endpoint_links()
            link = epl.list_posts(self.id)
            links = epl.create_links(link, self.postsCount, limit=limit)
        results = await self.scrape_manager.bulk_scrape(links)
        final_results = self.finalize_content_set(results)
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
            final_result = post_model.create_post(temp_result, self)
            if not final_result.author.id:
                final_result.author = create_user(final_result.__raw__["author"], self)
                pass
            return final_result
        return result

    async def get_messages(
        self,
        links: list[str] = [],
        limit: int = 10,
        offset_id: int = 0,
        cutoff_id: int | None = None,
        depth: int = 1,
        refresh: bool = True,
    ):
        result, status = await api_helper.default_data(self, refresh)
        if status:
            return result
        if self.is_deleted:
            return result
        temp_limit = limit
        link = endpoint_links(
            identifier=self.id, global_limit=temp_limit, global_offset=offset_id
        ).message_api
        results = await self.get_session_manager().bulk_json_requests([link])
        results = await api_helper.remove_errors(results)
        final_results = []
        if isinstance(results, list):
            results = [x for x in results if x]
            has_more = results[-1]["hasMore"] if results else False
            final_results = [x["list"] for x in results if "list" in x]
            final_results = list(chain.from_iterable(final_results))
            if has_more:
                temp_offset_id = final_results[-1]["id"]
                if not any(x for x in final_results if x["id"] == cutoff_id):
                    pass
                    results2 = await self.get_messages(
                        limit=temp_limit,
                        offset_id=temp_offset_id,
                        cutoff_id=cutoff_id,
                        depth=depth + 1,
                    )
                    final_results.extend(results2)
            if depth == 1:
                final_results = [
                    message_model.create_message(x, self) for x in final_results if x
                ]
            else:
                final_results.sort(key=lambda x: x["fromUser"]["id"], reverse=True)
            self.scrape_manager.scraped.Messages = final_results
        return final_results

    async def get_message_by_id(
        self,
        user_id: Optional[int] = None,
        message_id: Optional[int] = None,
        refresh: bool = True,
        limit: int = 10,
        offset: int = 0,
    ):
        if not user_id:
            user_id = self.id
        link = endpoint_links(
            identifier=user_id,
            identifier2=message_id,
            global_limit=limit,
            global_offset=offset,
        ).message_by_id
        response = await self.get_session_manager().json_request(link)
        if isinstance(response, dict):
            temp_response: dict[str, Any] = response
            results: list[dict[str, Any]] = [
                x for x in temp_response["list"] if x["id"] == message_id
            ]
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
        results = [create_story(x, self) for x in results]
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

        self.scrape_manager.scraped.Posts.extend(final_results)
        return final_results

    async def search_chat(
        self,
        identifier: int | str = "",
        text: str = "",
        refresh: bool = True,
        limit: int = 10,
        offset: int = 0,
    ):
        # Onlyfans can't do a simple search, so this is broken. If you want it to "work", don't use commas, or basically any mysql injection characters (lol)
        if identifier:
            identifier = parse.urljoin(str(identifier), "messages")
        else:
            identifier = self.id
        link = endpoint_links(
            identifier=identifier, text=text, global_limit=limit, global_offset=offset
        ).search_chat
        results = await self.get_session_manager().json_request(link)
        return results

    async def search_messages(
        self,
        identifier: int | str = "",
        text: str = "",
        refresh: bool = True,
        limit: int = 10,
        offset: int = 0,
    ):
        # Onlyfans can't do a simple search, so this is broken. If you want it to "work", don't use commas, or basically any mysql injection characters (lol)
        if identifier:
            identifier = parse.urljoin(str(identifier), "messages")
        text = parse.quote_plus(text)
        link = endpoint_links(
            identifier=identifier, text=text, global_limit=limit, global_offset=offset
        ).search_messages
        results = await self.get_session_manager().json_request(link)
        return results

    async def like(self, category: str, identifier: int):
        link = endpoint_links(identifier=category, identifier2=identifier).like
        results = await self.get_session_manager().json_request(link, method="POST")
        return results

    async def unlike(self, category: str, identifier: int):
        link = endpoint_links(identifier=category, identifier2=identifier).like
        results = await self.get_session_manager().json_request(link, method="DELETE")
        return results

    async def subscription_price(self):
        """
        Returns subscription price. This includes the promotional price.
        """
        subscription_price = self.subscribePrice
        if self.promotions:
            for promotion in self.promotions:
                promotion_price: int = promotion["price"]
                if promotion_price < subscription_price:
                    subscription_price = promotion_price
        return subscription_price

    async def get_promotions(self):
        return self.promotions

    async def buy_subscription(self):
        """
        This function will subscribe to a model. If the model has a promotion available, it will use it.
        """
        subscription_price = await self.subscription_price()
        x: dict[str, Any] = {
            "paymentType": "subscribe",
            "userId": self.id,
            "subscribeSource": "profile",
            "amount": subscription_price,
            "token": "",
            "unavailablePaymentGates": [],
        }
        if self.get_authed().creditBalance >= subscription_price:
            link = endpoint_links().pay
            result = await self.get_session_manager().json_request(
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

    async def get_avatar(self):
        return self.avatar

    async def get_header(self):
        return self.header

    async def is_subscribed(self):
        return not self.subscribedIsExpiredNow

    async def get_paid_contents(self, content_type: str | None = None):
        # REMINDER THAT YOU'LL HAVE TO REFRESH CONTENT
        final_paid_content: list[create_post | message_model.create_message] = []
        authed = self.get_authed()
        for paid_content in authed.paid_content:
            # Just use response to key function in ContentTypes
            if paid_content.author.id == self.id:
                if (
                    content_type is not None
                    and content_type.lower() != f"{paid_content.responseType}s"
                ):
                    continue
                final_paid_content.append(paid_content)
        return final_paid_content

    async def has_socials(self):
        # If error message, this means the user has socials, but we have to subscribe to see them
        result = bool(
            await self.get_session_manager().json_request(
                endpoint_links(self.id).socials
            )
        )
        return result

    async def get_socials(self):
        results: list[dict[str, Any]] | dict[
            str, Any
        ] = await self.get_session_manager().json_request(
            endpoint_links(self.id).socials
        )
        if "error" in results:
            results = []
        assert isinstance(results, list)
        return results

    async def get_spotify(self):
        if self.isSpotifyConnected:
            result: dict[str, Any] = await self.get_session_manager().json_request(
                endpoint_links(self.id).spotify
            )
            if "error" in result:
                result = {}
            return result

    async def has_spotify(self):
        # If error message, this means the user has socials, but we have to subscribe to see them
        result = bool(
            await self.get_session_manager().json_request(
                endpoint_links(self.id).spotify
            )
        )
        return result
