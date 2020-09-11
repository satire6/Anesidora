PRODUCT_RELEASE :=

ifeq '${LANGUAGE}' 'japanese'
	PRODUCT_RELEASE := _JP
endif
ifeq '${LANGUAGE}' 'portuguese'
	PRODUCT_RELEASE := _BR
endif
ifeq '${LANGUAGE}' 'french'
	PRODUCT_RELEASE := _FR
endif
