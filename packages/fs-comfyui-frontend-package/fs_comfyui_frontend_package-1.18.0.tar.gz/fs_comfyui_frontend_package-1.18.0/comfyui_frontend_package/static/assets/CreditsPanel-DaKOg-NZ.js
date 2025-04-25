var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
import { defineComponent, computed, ref, openBlock, createBlock, withCtx, createBaseVNode, toDisplayString, createVNode, unref, createElementBlock, createCommentVNode, normalizeClass } from "./vendor-vue-B7YUw5vA.js";
import { script$9 as script, script$34 as script$1, script$24 as script$2, script$1 as script$3, script$60 as script$4, script$61 as script$5, script$18 as script$6 } from "./vendor-primevue-mBmZOOxc.js";
import { useI18n } from "./vendor-vue-i18n-CdFxvEOa.js";
import { useDialogService, useFirebaseAuthStore, useFirebaseAuthService, formatMetronomeCurrency } from "./index-DjD6e2ml.js";
const _hoisted_1 = { class: "flex flex-col h-full" };
const _hoisted_2 = { class: "text-2xl font-bold mb-2" };
const _hoisted_3 = { class: "flex flex-col gap-2" };
const _hoisted_4 = { class: "text-sm font-medium text-muted" };
const _hoisted_5 = { class: "flex justify-between items-center" };
const _hoisted_6 = {
  key: 0,
  class: "flex items-center gap-1"
};
const _hoisted_7 = { class: "flex items-center gap-2" };
const _hoisted_8 = {
  key: 1,
  class: "flex items-center gap-1"
};
const _hoisted_9 = { class: "text-3xl font-bold" };
const _hoisted_10 = { class: "flex flex-row items-center" };
const _hoisted_11 = {
  key: 1,
  class: "text-xs text-muted"
};
const _hoisted_12 = { class: "flex justify-between items-center mt-8" };
const _hoisted_13 = {
  key: 0,
  class: "flex-grow"
};
const _hoisted_14 = { class: "text-sm font-medium" };
const _hoisted_15 = { class: "text-xs text-muted" };
const _hoisted_16 = { class: "flex flex-row gap-2" };
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "CreditsPanel",
  setup(__props) {
    const { t } = useI18n();
    const dialogService = useDialogService();
    const authStore = useFirebaseAuthStore();
    const authService = useFirebaseAuthService();
    const loading = computed(() => authStore.loading);
    const balanceLoading = computed(() => authStore.isFetchingBalance);
    const formattedBalance = computed(() => {
      if (!authStore.balance) return "0.00";
      return formatMetronomeCurrency(authStore.balance.amount_micros, "usd");
    });
    const formattedLastUpdateTime = computed(
      () => authStore.lastBalanceUpdateTime ? authStore.lastBalanceUpdateTime.toLocaleString() : ""
    );
    const handlePurchaseCreditsClick = /* @__PURE__ */ __name(() => {
      dialogService.showTopUpCreditsDialog();
    }, "handlePurchaseCreditsClick");
    const handleCreditsHistoryClick = /* @__PURE__ */ __name(async () => {
      await authService.accessBillingPortal();
    }, "handleCreditsHistoryClick");
    const handleMessageSupport = /* @__PURE__ */ __name(() => {
      dialogService.showIssueReportDialog({
        title: t("issueReport.contactSupportTitle"),
        subtitle: t("issueReport.contactSupportDescription"),
        panelProps: {
          errorType: "BillingSupport",
          defaultFields: ["Workflow", "Logs", "SystemStats", "Settings"]
        }
      });
    }, "handleMessageSupport");
    const handleFaqClick = /* @__PURE__ */ __name(() => {
      window.open("https://www.comfy.org/faq", "_blank");
    }, "handleFaqClick");
    const creditHistory = ref([]);
    return (_ctx, _cache) => {
      return openBlock(), createBlock(unref(script$6), {
        value: "Credits",
        class: "credits-container h-full"
      }, {
        default: withCtx(() => [
          createBaseVNode("div", _hoisted_1, [
            createBaseVNode("h2", _hoisted_2, toDisplayString(_ctx.$t("credits.credits")), 1),
            createVNode(unref(script)),
            createBaseVNode("div", _hoisted_3, [
              createBaseVNode("h3", _hoisted_4, toDisplayString(_ctx.$t("credits.yourCreditBalance")), 1),
              createBaseVNode("div", _hoisted_5, [
                balanceLoading.value ? (openBlock(), createElementBlock("div", _hoisted_6, [
                  createBaseVNode("div", _hoisted_7, [
                    createVNode(unref(script$1), {
                      shape: "circle",
                      width: "1.5rem",
                      height: "1.5rem"
                    })
                  ]),
                  _cache[1] || (_cache[1] = createBaseVNode("div", { class: "flex-1" }, null, -1)),
                  createVNode(unref(script$1), {
                    width: "8rem",
                    height: "2rem"
                  })
                ])) : (openBlock(), createElementBlock("div", _hoisted_8, [
                  createVNode(unref(script$2), {
                    severity: "secondary",
                    icon: "pi pi-dollar",
                    rounded: "",
                    class: "text-amber-400 p-1"
                  }),
                  createBaseVNode("div", _hoisted_9, toDisplayString(formattedBalance.value), 1)
                ])),
                loading.value ? (openBlock(), createBlock(unref(script$1), {
                  key: 2,
                  width: "2rem",
                  height: "2rem"
                })) : (openBlock(), createBlock(unref(script$3), {
                  key: 3,
                  label: _ctx.$t("credits.purchaseCredits"),
                  loading: loading.value,
                  onClick: handlePurchaseCreditsClick
                }, null, 8, ["label", "loading"]))
              ]),
              createBaseVNode("div", _hoisted_10, [
                balanceLoading.value ? (openBlock(), createBlock(unref(script$1), {
                  key: 0,
                  width: "12rem",
                  height: "1rem",
                  class: "text-xs"
                })) : formattedLastUpdateTime.value ? (openBlock(), createElementBlock("div", _hoisted_11, toDisplayString(_ctx.$t("credits.lastUpdated")) + ": " + toDisplayString(formattedLastUpdateTime.value), 1)) : createCommentVNode("", true),
                createVNode(unref(script$3), {
                  icon: "pi pi-refresh",
                  text: "",
                  size: "small",
                  severity: "secondary",
                  onClick: _cache[0] || (_cache[0] = () => unref(authService).fetchBalance())
                })
              ])
            ]),
            createBaseVNode("div", _hoisted_12, [
              createVNode(unref(script$3), {
                label: _ctx.$t("credits.invoiceHistory"),
                text: "",
                severity: "secondary",
                icon: "pi pi-arrow-up-right",
                loading: loading.value,
                onClick: handleCreditsHistoryClick
              }, null, 8, ["label", "loading"])
            ]),
            creditHistory.value.length > 0 ? (openBlock(), createElementBlock("div", _hoisted_13, [
              createVNode(unref(script$5), {
                value: creditHistory.value,
                "show-headers": false
              }, {
                default: withCtx(() => [
                  createVNode(unref(script$4), {
                    field: "title",
                    header: _ctx.$t("g.name")
                  }, {
                    body: withCtx(({ data }) => [
                      createBaseVNode("div", _hoisted_14, toDisplayString(data.title), 1),
                      createBaseVNode("div", _hoisted_15, toDisplayString(data.timestamp), 1)
                    ]),
                    _: 1
                  }, 8, ["header"]),
                  createVNode(unref(script$4), {
                    field: "amount",
                    header: _ctx.$t("g.amount")
                  }, {
                    body: withCtx(({ data }) => [
                      createBaseVNode("div", {
                        class: normalizeClass([
                          "text-base font-medium text-center",
                          data.isPositive ? "text-sky-500" : "text-red-400"
                        ])
                      }, toDisplayString(data.isPositive ? "+" : "-") + "$" + toDisplayString(unref(formatMetronomeCurrency)(data.amount, "usd")), 3)
                    ]),
                    _: 1
                  }, 8, ["header"])
                ]),
                _: 1
              }, 8, ["value"])
            ])) : createCommentVNode("", true),
            createVNode(unref(script)),
            createBaseVNode("div", _hoisted_16, [
              createVNode(unref(script$3), {
                label: _ctx.$t("credits.faqs"),
                text: "",
                severity: "secondary",
                icon: "pi pi-question-circle",
                onClick: handleFaqClick
              }, null, 8, ["label"]),
              createVNode(unref(script$3), {
                label: _ctx.$t("credits.messageSupport"),
                text: "",
                severity: "secondary",
                icon: "pi pi-comments",
                onClick: handleMessageSupport
              }, null, 8, ["label"])
            ])
          ])
        ]),
        _: 1
      });
    };
  }
});
export {
  _sfc_main as default
};
//# sourceMappingURL=CreditsPanel-DaKOg-NZ.js.map
