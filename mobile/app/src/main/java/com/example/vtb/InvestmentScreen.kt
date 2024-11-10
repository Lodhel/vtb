package com.example.vtb

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.EaseInOutCubic
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ScrollableTabRow
import androidx.compose.material3.Tab
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.vtb.ui.theme.*
import com.example.vtb.ui.theme.VTBTheme
import ir.ehsannarmani.compose_charts.LineChart
import ir.ehsannarmani.compose_charts.PieChart
import ir.ehsannarmani.compose_charts.models.AnimationMode
import ir.ehsannarmani.compose_charts.models.DotProperties
import ir.ehsannarmani.compose_charts.models.DrawStyle
import ir.ehsannarmani.compose_charts.models.GridProperties
import ir.ehsannarmani.compose_charts.models.HorizontalIndicatorProperties
import ir.ehsannarmani.compose_charts.models.IndicatorCount
import ir.ehsannarmani.compose_charts.models.IndicatorPosition
import ir.ehsannarmani.compose_charts.models.LabelHelperProperties
import ir.ehsannarmani.compose_charts.models.LabelProperties
import ir.ehsannarmani.compose_charts.models.Line
import ir.ehsannarmani.compose_charts.models.Pie
import kotlinx.coroutines.delay

@Composable
fun InvestmentScreen(
    modifier: Modifier = Modifier
) {
    var tabIndex by remember { mutableStateOf(0) }
    val tabs = listOf("Мой капитал", "Реккомендации")

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(color = MaterialTheme.colorScheme.background)
    ) {
        item {
            Text(
                "Инвестиции",
                fontWeight = FontWeight.Bold,
                fontSize = 24.sp,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                textAlign = TextAlign.Center,
                color = MaterialTheme.colorScheme.onBackground
            )
        }
        item {
            Text(
                "Быстрые действия",
                fontWeight = FontWeight.Bold,
                fontSize = 20.sp,
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                color = MaterialTheme.colorScheme.onBackground
            )
        }
        item {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .weight(1f)
                        .padding(4.dp)
                        .background(
                            color = MaterialTheme.colorScheme.surface,
                            shape = RoundedCornerShape(24.dp)
                        )
                ) { }
                Column(
                    modifier = Modifier
                        .fillMaxHeight()
                        .weight(1f),
                    verticalArrangement = Arrangement.SpaceEvenly
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f)
                            .padding(4.dp)
                            .background(
                                color = MaterialTheme.colorScheme.surface,
                                shape = RoundedCornerShape(24.dp)
                            )
                    )
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f)
                            .padding(4.dp)
                            .background(
                                color = MaterialTheme.colorScheme.surface,
                                shape = RoundedCornerShape(24.dp)
                            )
                    )
                }
            }
        }
        item {
            Button(
                onClick = {},
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                colors = ButtonDefaults.buttonColors().copy(containerColor = Surface),
                shape = RoundedCornerShape(14.dp)
            ) { Text("Все сервисы") }
        }
        item {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 14.dp, bottom = 40.dp)
                    .background(
                        color = MaterialTheme.colorScheme.surface,
                        shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp)
                    ),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Box(
                    modifier = Modifier
                        .padding(top = 20.dp)
                        .width(38.dp)
                        .height(3.dp)
                        .background(Blue, RoundedCornerShape(10.dp))
                )
                ScrollableTabRow(
                    edgePadding = 0.dp,
                    containerColor = Transparent,
                    indicator = {},
                    divider = {},
                    selectedTabIndex = tabIndex
                ) {
                    tabs.forEachIndexed { index, title ->
                        Tab(
                            text = {
                                Text(
                                    title,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 20.sp
                                )
                            },
                            selected = tabIndex == index,
                            onClick = { tabIndex = index },
                            selectedContentColor = MaterialTheme.colorScheme.onSurface,
                            unselectedContentColor = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
                when (tabIndex) {
                    0 -> MyCapital()
                    1 -> Recommendations()
                }
            }
        }
    }
}

@Composable
fun Recommendations() {
    Inflation()
    AnalystsAdvices()
    VtbAnalytics()
    Button(
        onClick = {},
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 6.dp),
        colors = ButtonDefaults.buttonColors().copy(containerColor = Surface),
        shape = RoundedCornerShape(14.dp)
    ) { Text("Все предложения", fontSize = 16.sp) }
    AssetReturn()
}

@Composable
fun MyCapital() {
    Potential()
    Expenses()
}

@Composable
fun Inflation() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(10.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            )
    ) {
        Text(
            "Инфляция",
            fontWeight = FontWeight.Bold,
            fontSize = 20.sp,
            modifier = Modifier.padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 8.dp),
            color = MaterialTheme.colorScheme.onSurface
        )
        InflationChart(
            listOf(11.76, 10.97, 3.51, 2.30, 2.50, 3.24, 4.30, 5.13, 6.00, 6.68, 7.47, 7.42),
            listOf(13.76, 12.97, 5.51, 4.30, 4.50, 5.24, 6.30, 7.13, 8.00, 8.68, 9.47, 9.42)
        )
    }
}

@Composable
fun InflationChart(inflation: List<Double>, key_rate: List<Double>) {
    LineChart(
        gridProperties = GridProperties(false),
        labelProperties = LabelProperties(
            enabled = true,
            textStyle = TextStyle.Default.copy(color = MaterialTheme.colorScheme.onSurface),
            labels = listOf("Сейчас", "3 мес", "6 мес", "1 год")
        ),
        indicatorProperties = HorizontalIndicatorProperties(
            enabled = true,
            textStyle = TextStyle.Default.copy(color = MaterialTheme.colorScheme.onSurface),
            position = IndicatorPosition.Horizontal.Start,
            padding = 4.dp
        ),
        labelHelperProperties = LabelHelperProperties(enabled = false),
        curvedEdges = false,
        modifier = Modifier
            .fillMaxWidth()
            .height(200.dp)
            .padding(12.dp),
        data = remember {
            listOf(
                Line(
                    label = "",
                    values = inflation,
                    color = SolidColor(Teal),
                    strokeAnimationSpec = tween(2000, easing = EaseInOutCubic),
                    drawStyle = DrawStyle.Stroke(width = 2.dp),
                ),
                Line(
                    label = "",
                    values = key_rate,
                    color = SolidColor(Blue),
                    strokeAnimationSpec = tween(2000, easing = EaseInOutCubic),
                    drawStyle = DrawStyle.Stroke(width = 2.dp),
                )
            )
        },
        animationMode = AnimationMode.Together(delayBuilder = {
            it * 500L
        }),
    )
}

@Composable
fun AssetReturn() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(10.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            )
    ) {
        Text(
            "Доходность активов",
            fontWeight = FontWeight.Bold,
            fontSize = 20.sp,
            modifier = Modifier.padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 8.dp),
            color = MaterialTheme.colorScheme.onSurface
        )
        AssetReturnItem("Газпром", Teal, 28, 443, "низкий", true)
        AssetReturnItem("ВК", Blue, 2, 43, "высокий", false)
    }
}

@Composable
fun AssetReturnItem(
    name: String,
    ic_color: Color,
    assetReturn: Int,
    forecastPrice: Int,
    risk: String,
    isRecommended: Boolean
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            )
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                name,
                fontWeight = FontWeight.Bold,
                fontSize = 24.sp,
                color = MaterialTheme.colorScheme.onSurface
            )
            Box(
                Modifier
                    .size(50.dp)
                    .background(ic_color, RoundedCornerShape(100))
            )
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Доходность", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
            Text("$assetReturn%", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Прогнозная цена", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
            Text("$forecastPrice р", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Риск", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
            Text(risk, color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Рекомендация", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
            Text(
                if (isRecommended) "покупать" else "не покупать",
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 12.sp,
                modifier = Modifier
                    .background(if (isRecommended) Blue else Orange, RoundedCornerShape(24.dp))
                    .padding(horizontal = 4.dp)
            )
        }
    }
}

@Composable
fun AnalystsAdvices() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(10.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            )
    ) {
        Text(
            "Советуют аналитики",
            fontWeight = FontWeight.Bold,
            fontSize = 20.sp,
            modifier = Modifier.padding(top = 16.dp, start = 16.dp, end = 16.dp),
            color = MaterialTheme.colorScheme.onSurface
        )
        LazyRow(modifier = Modifier.padding(9.dp)) {
            items(5) {
                for (color in listOf(Red, Blue, Black, Pink, Grey)) {
                    Box(
                        Modifier
                            .padding(7.dp)
                            .size(60.dp)
                            .background(color, RoundedCornerShape(100))
                    )
                }
            }
        }
    }
}

@Composable
fun VtbAnalytics() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(10.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            )
    ) {
        Text(
            "Аналитика ВТБ",
            fontWeight = FontWeight.Bold,
            fontSize = 20.sp,
            modifier = Modifier.padding(top = 16.dp, start = 16.dp, end = 16.dp, bottom = 4.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            "Долгосрочные надежды",
            fontWeight = FontWeight.Bold,
            fontSize = 20.sp,
            modifier = Modifier.padding(start = 16.dp, end = 16.dp, bottom = 8.dp),
            color = MaterialTheme.colorScheme.onSurface
        )
        LongTermInvestItem()
    }
}

@Composable
fun LongTermInvestItem() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            )
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            Modifier
                .size(60.dp)
                .background(Black, RoundedCornerShape(100))
        )
        Column(
            modifier = Modifier
                .weight(1f)
                .padding(start = 8.dp)
        ) {
            Text(
                "Uber",
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
            Text("Сегодня", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
        }
        Column(modifier = Modifier.weight(1f)) {
            Text(
                "рост до 30%",
                color = MaterialTheme.colorScheme.onSurface,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
            Text("за 6 месяцев", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
        }
    }
}

@Composable
fun Expenses(
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(10.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            ),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            "Расходы и доходы",
            fontWeight = FontWeight.Bold,
            fontSize = 20.sp,
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            color = MaterialTheme.colorScheme.onSurface
        )
        ExpensesChart(
            data = listOf(
                Pie(label = "ЖКХ", data = 8900.0, color = Purple),
                Pie(label = "Кино", data = 2500.0, color = Blue),
                Pie(label = "Подарки", data = 15000.0, color = Orange),
                Pie(label = "Продукты", data = 10600.0, color = Teal),
            )
        )
    }
}

@Composable
fun ExpensesChart(
    data: List<Pie>,
) {
    PieChart(
        modifier = Modifier.size(200.dp),
        data = remember { data },
        onPieClick = {},
        selectedScale = 1.2f,
        scaleAnimEnterSpec = spring<Float>(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        ),
        colorAnimEnterSpec = tween(300),
        colorAnimExitSpec = tween(300),
        scaleAnimExitSpec = tween(300),
        spaceDegreeAnimExitSpec = tween(300),
        style = Pie.Style.Stroke()
    )

    DetailsPieChart(data)
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun DetailsPieChart(
    data: List<Pie>,
) {
    FlowRow(
        modifier = Modifier
            .padding(vertical = 20.dp, horizontal = 12.dp)
            .fillMaxWidth()
    ) {
        data.forEachIndexed { index, value ->
            DetailsPieChartItem(
                data = value.label + " " + value.data.toInt(),
                color = value.color
            )
        }
    }
}

@Composable
fun DetailsPieChartItem(
    data: String,
    color: Color
) {
    Box(
        modifier = Modifier
            .padding(4.dp)
            .background(color = color, shape = RoundedCornerShape(40.dp))
    ) {
        Text(
            data,
            color = Color.White,
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp)
        )
    }
}

@Composable
fun Potential() {
    var potentialTabIndex by remember { mutableStateOf(0) }
    val potentialTabs = listOf("200р", "300р", "400р", "500р", "1000р", "5000р", "своя сумма")

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(10.dp)
            .background(
                color = MaterialTheme.colorScheme.surface,
                shape = RoundedCornerShape(24.dp)
            )
    ) {
        Text(
            "Потенциал",
            fontWeight = FontWeight.Bold,
            fontSize = 20.sp,
            modifier = Modifier.padding(16.dp),
            color = MaterialTheme.colorScheme.onSurface
        )

        PotentialChart(5.0)

        ScrollableTabRow(
            edgePadding = 0.dp,
            modifier = Modifier.padding(12.dp),
            containerColor = Transparent,
            indicator = {},
            divider = {},
            selectedTabIndex = potentialTabIndex
        ) {
            potentialTabs.forEachIndexed { index, title ->
                Tab(
                    text = {
                        Text(
                            title,
                            fontSize = 14.sp
                        )
                    },
                    modifier = Modifier
                        .background(
                            color = if (potentialTabIndex == index) Blue else Surface,
                            shape = RoundedCornerShape(40.dp)
                        )
                        .height(35.dp),
                    selected = potentialTabIndex == index,
                    onClick = { potentialTabIndex = index },
                    selectedContentColor = MaterialTheme.colorScheme.onSurface,
                    unselectedContentColor = MaterialTheme.colorScheme.onSurface
                )
            }
        }
        when (potentialTabIndex) {

        }
    }
}

@Composable
fun PotentialChart(endingPoint: Double) {
    var textVisible by remember {
        mutableStateOf(false)
    }
    LaunchedEffect(key1 = Unit, block = {
        delay(600L)
        textVisible = true
    })
    Box(
        contentAlignment = Alignment.TopCenter,
        modifier = Modifier.fillMaxWidth()
    ) {
        LineChart(
            gridProperties = GridProperties(false),
            indicatorProperties = HorizontalIndicatorProperties(
                enabled = true,
                textStyle = TextStyle.Default.copy(color = MaterialTheme.colorScheme.onSurface),
                count = IndicatorCount.CountBased(count = endingPoint.toInt()),
                position = IndicatorPosition.Horizontal.Start,
                padding = 4.dp,
                contentBuilder = { indicator ->
                    "%d".format(indicator.toInt()) + " млн"
                }),
            labelProperties = LabelProperties(
                enabled = true,
                textStyle = TextStyle.Default.copy(color = MaterialTheme.colorScheme.onSurface),
                labels = listOf("Сейчас", "3 мес", "6 мес", "1 год")
            ),
            labelHelperProperties = LabelHelperProperties(enabled = false),
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp)
                .padding(12.dp),
            data = remember {
                listOf(
                    Line(
                        label = "",
                        values = listOf(0.0, endingPoint),
                        color = SolidColor(Blue),
                        firstGradientFillColor = Blue.copy(alpha = .5f),
                        secondGradientFillColor = Color.Transparent,
                        strokeAnimationSpec = tween(2000, easing = EaseInOutCubic),
                        gradientAnimationDelay = 1000,
                        drawStyle = DrawStyle.Stroke(width = 2.dp),
                        dotProperties = DotProperties(
                            enabled = true,
                            color = SolidColor(Blue),
                            radius = 7.dp,
                        )
                    )
                )
            },
            animationMode = AnimationMode.Together(delayBuilder = {
                it * 500L
            }),
            maxValue = endingPoint.toInt() * 2.0
        )
        AnimatedVisibility(
            visible = textVisible,
            enter = fadeIn(animationSpec = tween(durationMillis = 3000))
        ) {
            Column(
                modifier = Modifier
                    .background(
                        color = MaterialTheme.colorScheme.surface,
                        shape = RoundedCornerShape(14.dp)
                    )
                    .padding(horizontal = 12.dp, vertical = 4.dp),
                verticalArrangement = Arrangement.spacedBy((-3).dp),
            ) {
                Text("цель", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
                Text("5 890 000 р", modifier = Modifier.drawBehind {
                    val strokeWidthPx = 2.dp.toPx()
                    val verticalOffset = size.height
                    drawLine(
                        color = Blue,
                        strokeWidth = strokeWidthPx,
                        start = Offset(0f, verticalOffset),
                        end = Offset(size.width, verticalOffset)
                    )
                }, color = MaterialTheme.colorScheme.onSurface, fontSize = 20.sp)
                Row(horizontalArrangement = Arrangement.SpaceBetween) {
                    Column(verticalArrangement = Arrangement.spacedBy((-8).dp)) {
                        Text("вклад", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
                        Text(
                            "34 000",
                            color = MaterialTheme.colorScheme.onSurface,
                            fontSize = 12.sp
                        )
                    }
                    Spacer(modifier = Modifier.width(20.dp))
                    Column(verticalArrangement = Arrangement.spacedBy((-8).dp)) {
                        Text("доход", color = MaterialTheme.colorScheme.onSurface, fontSize = 12.sp)
                        Text(
                            "124 000",
                            color = MaterialTheme.colorScheme.onSurface,
                            fontSize = 12.sp
                        )
                    }
                }
            }
        }

    }
}

@Preview(showBackground = true)
@Composable
fun InvestmentPreview() {
    VTBTheme(true) {
        InvestmentScreen()
    }
}
